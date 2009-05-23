#!/usr/bin/perl -w
use strict;
use DBI;
BEGIN { unshift @INC,("/home/agimenez/metaf2xml/lib"); }
use DBD::Pg qw(:pg_types);
use metaf2xml::parser;

my %convert = ('KT' => 1.85200, "KPH" => 1, "MPS" => 3.6);

main(scalar(@ARGV), @ARGV);

sub main {
    my ($argc, @argv) = @_;
    #my %report = metaf2xml::parser::parseReport("AAXX 25004 86086 21670 70902 10260 20230 40079 56013 71399 81970 333 10350 60011 81940", 0, 1);
    #process(\%report);
    $ENV{PGSYSCONFDIR} = "./";
    if ($argc > 0) {
        my $dbh = DBI->connect("dbi:Pg:service=telemetria", '', '', {AutoCommit => 0, RaiseError => 1})
                  || die "No me pude conectar";
        my $estacion = $dbh->prepare("SELECT id, nombre FROM estacion WHERE comentario ~* ?");
        my $medida = $dbh->prepare("INSERT INTO medida (estacion_id, variable_id, tiempo, valor) VALUES (?, ?, ?, ?)");
        my $last = "";
        my $lastStationId = 0;
        my $lastCount = -1;
        my $tiempo = "";
        open(FH, ">noreg.log");
        my $station;
        my %estaciones = ();
        eval {
            foreach my $line (<>) {
                next if ($line =~ m/^#|^$/);
                chomp ($line); 
                $line =~ s/NIL|=//g;
                if ($line =~ /^[0-9]+/) {
                    # Process
                    if ($last) {
                        my ($fecha, $data) = split / /, $last, 2;
                        my %report = metaf2xml::parser::parseReport($data, 0, 1);
                        if (%report && !exists($report{"ERROR"})) {
                            my @result = processSynop(\%report);
                            my @date = split /^([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})/, $fecha;
                            $fecha = "$date[1]-$date[2]-$date[3] $date[4]:$date[5]:00+00";
                            if ($tiempo ne "$date[1]-$date[2]") {
                                $tiempo = "$date[1]-$date[2]";
                                print "\n === $tiempo === \n"
                            }
                            if ($lastStationId != $result[0]) {
                                $lastStationId = $result[0];
                                if (!exists($estaciones{$lastStationId})) {
                                    $estacion->execute($lastStationId);
                                    $station = $estacion->fetch();
                                    if ($station) {
                                        $estaciones{$lastStationId} = [${$station}[0], ${$station}[1]];
                                    }
                                }
                                else {
                                    $station = $estaciones{$lastStationId};
                                }
                                if ($station) {
                                    if ($lastCount > -1) {
                                        print " ($lastCount) \n";
                                    }
                                    print "== Estación ${$station}[0] - ${$station}[1] ==\n";
                                }
                                else {
                                    print FH "== Estación $result[0] no registrada ==\n";
                                }
                                $lastCount = 0;
                            }
                            if ($station) {
                                #printf "$fecha %d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", @result;
                                if ($result[1] != -1) { # DD
                                    $medida->execute($${station}[0], 'DD', $fecha, $result[1]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                                if ($result[2] != -1) { # FF
                                    $medida->execute($${station}[0], 'FF', $fecha, $result[2]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                                if ($result[3] != 100) { # T
                                    $medida->execute($${station}[0], 'T', $fecha, $result[3]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                                if ($result[4] != 100) { # TD
                                    $medida->execute($${station}[0], 'TD', $fecha, $result[4]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                                if ($result[5] != -1) { # RH
                                    $medida->execute($${station}[0], 'RH', $fecha, $result[5]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                                if ($result[6] != -1) { # P
                                    $medida->execute($${station}[0], 'P', $fecha, $result[6]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                                if ($result[7] != -1) { # SLP
                                    $medida->execute($${station}[0], 'SLP', $fecha, $result[7]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                                if ($result[8] != -1) { # PREC
                                    $medida->execute($${station}[0], 'PCP', $fecha, $result[8]) || die("Error al insertar datos");
                                    $lastCount++;
                                }
                            }
                            else {
                                printf FH "$fecha %d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", @result;
                            }
                        }
                        else {
                            print STDERR $report{"ERROR"} if !exists($report{"ERROR"});
                        }
                    }
                    $last = $line;
                }
                else {
                    $line =~ s/^\s+//;
                    $last = $last . " " . $line;
                }
            }
        };
        if ($@) {
            $dbh->rollback();
        }
        else {
            $dbh->commit();
        }
        close(FH);
        $estacion->finish();
        $medida->finish();
        $dbh->disconnect();
    }
    else {
        print "Especificar la ruta\n";
    }
}

sub processSynop {
    my ($r) = @_;
    # Valores Invalidos (sin datos) none
    # ID (SYNOP) = 0
    # DD [0, 360] = -1
    # FF [0, inf] = -1
    # T [-99.9, 99.9] = 100
    # TD [-99.9, 99.9] = 100
    # P [1000, 1999,9] = -1
    # SLP [1000, 1999,9] = -1
    # RH [0, 100] = -1
    # PREC [1, 989] = -1
    my ($id, $dd, $ff, $t, $td, $p, $slp, $rh, $prec) = (0, -1, -1, 100, 100, -1, -1, -1, -1);
    my $unit = "KPH";
    my %report = %$r;
    $id = $report{'obsStationId'}{'id'};
    my %viento = %{$report{'sfcWind'}{'wind'}} if (exists($report{'sfcWind'}));
    if (%viento) {
        $dd = $viento{'dir'}{'v'} if (exists($viento{'dir'})); 
        $unit = $viento{'speed'}{'u'} if (exists($viento{'speed'}{'u'}));
        $ff = $viento{'speed'}{'v'} if (exists($viento{'speed'}{'v'}));
        if (!defined($convert{$unit}) || !defined($ff)) {
            print STDERR "Unidad $id $ff $unit \n";
        }
    }
    my %temp = %{$report{'temperature'}} if (exists($report{'temperature'}));
    if (%temp) {
        $t =$temp{'air'}{'temp'}{'v'} if (exists($temp{'air'}{'temp'}{'v'}));
        $td = $temp{'dewpoint'}{'temp'}{'v'} if (exists($temp{'dewpoint'}{'temp'}{'v'}));
        if (exists($temp{'relHumid1'}) && 
            exists($temp{'relHumid2'}) &&
            exists($temp{'relHumid3'}) &&
            exists($temp{'relHumid4'}) ) {
            $rh = $temp{'relHumid1'};
        }
    }
    $p = $report{'stationPressure'}{'hPa'} if (exists($report{'stationPressure'}{'hPa'}));
    $slp = $report{'SLPhPa'}{'hPa'} if (exists($report{'SLPhPa'}{'hPa'}));
    if ($report{'precipInd'}{'s'} ne '/' && $report{'precipInd'}{'s'} == 2 && exists($report{'section3'})) {
        my ($prec_sec, %prec_info, %prec_now);
        for $prec_sec (@{$report{'section3'}}) {
            %prec_now = %$prec_sec;
            if (exists($prec_now{'precipHourly'})) {
                %prec_info = %prec_now;
            }
        }
        $prec = $prec_info{'precipHourly'}{'precipAmount'}{'v'} if (exists($prec_info{'precipHourly'}{'precipAmount'}));
    }
    elsif ($report{'precipInd'}{'s'} ne '/' && ($report{'precipInd'}{'s'} == 0 || $report{'precipInd'}{'s'} == 1)) {
        $prec = $report{'precipHourly'}{'precipAmount'}{'v'} if (exists($report{'precipHourly'}{'precipAmount'}));
    }
    #printf STDERR "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2,%.2f\n", $id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp,$prec;
    return ($id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp,$prec);
}