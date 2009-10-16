#!/usr/bin/perl -w
use strict;
use DBI;
BEGIN { unshift @INC,("/home/agimenez/metaf2xml/lib"); }
use metaf2xml::parser;

my %convert = ('KT' => 1.85200, "KPH" => 1, "MPS" => 3.6);

main(scalar(@ARGV), @ARGV);

sub main {
    my ($argc, @argv) = @_;
    #my %report = metaf2xml::parser::parseReport("AAXX 25004 86086 21670 70902 10260 20230 40079 56013 71399 81970 333 10350 60011 81940", 0, 1);
    #process(\%report);
    if ($argc > 0) {
        my $dbh = DBI->connect("dbi:mysql:database=cemet;host=localhost", 'cemet', 'c3m3t', {AutoCommit => 0, RaiseError => 1})
                  || die "No me pude conectar";
        my $estacion = $dbh->prepare("SELECT id, nombre FROM estacion WHERE codigo REGEXP ?");
        my $sensor = $dbh->prepare("SELECT id FROM sensor WHERE estacion_id = ? AND variable_id = ?");
        my $medida = $dbh->prepare("INSERT INTO medida (sensor_id, tiempo, valor) VALUES (?, ?, ?)");
        my $last = "";
        my $lastStationId = "";
        my $lastCount = -1;
        my $tiempo = "";
        open(FH, ">noreg_my.log");
        my $station;
        my $sens;
        my %estaciones = ();
        my $last_time = "";
        eval {
            foreach my $line (<>) {
                chomp $line;
                my ($fecha, $data) = split / /, $line, 2;
                my %report = metaf2xml::parser::parseReport($data, 0, 0);
                if (%report && !exists($report{"ERROR"})) {
                    my @result = processMetar(\%report);
                    my @date = split /^([0-9]{4})\/([0-9]{2})\/([0-9]{2})/, $fecha;
                    my ($hour,$minute) = ($report{'obsTime'}{'hour'}, $report{'obsTime'}{'minute'});
                    $fecha = "$date[1]-$date[2]-$date[3] $hour:$minute:00+00";
                    if ($tiempo ne "$date[1]-$date[2]") {
                        $tiempo = "$date[1]-$date[2]";
                        print "\n === $tiempo === \n"
                    }
                    if ($lastStationId ne $result[0]) {
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
                    if ($station and $fecha ne $last_time) {
                        #printf "$fecha %s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", @result;
                        $last_time = $fecha;
                        if ($result[1] != -1) { # DD
                            $sensor->execute($$station[0], 'DD');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[1]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                        if ($result[2] != -1) { # FF
                            $sens = $sensor->execute($$station[0], 'FF');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[2]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                        if ($result[3] != 100) { # T
                            $sens = $sensor->execute($$station[0], 'T');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[3]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                        if ($result[4] != 100) { # TD
                            $sens = $sensor->execute($$station[0], 'TD');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[4]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                        if ($result[5] != -1) { # RH
                            $sens = $sensor->execute($$station[0], 'RH');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[5]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                        if ($result[6] != -1) { # P
                            $sens = $sensor->execute($$station[0], 'P');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[6]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                        if ($result[7] != -1) { # SLP
                            $sens = $sensor->execute($$station[0], 'SLP');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[7]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                        if ($result[8] != -1) { # PREC
                            $sens = $sensor->execute($$station[0], 'PCP');
                            $sens = $sensor->fetch();
                            $medida->execute($${sens}[0], $fecha, $result[8]) || die("Error al insertar datos");
                            $lastCount++;
                        }
                    }
                    else {
                        printf FH "$fecha %s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", @result;
                    }
                }
                else {
                    print STDERR $report{"ERROR"} . "\n" if !exists($report{"ERROR"});
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
        $sensor->finish();
        $medida->finish();
        $dbh->disconnect();
    }
    else {
        print "Especificar la ruta\n";
    }
}

sub processMetar {
    my ($r) = @_;
    # Valores Invalidos (sin datos) none
    # ID (METAR) = ""
    # DD [0, 360] = -1
    # FF [0, inf] = -1
    # T [-99.9, 99.9] = 100
    # TD [-99.9, 99.9] = 100
    # P [1000, 1999,9] = -1
    # SLP [1000, 1999,9] = -1
    # RH [0, 100] = -1
    # PREC [1, 989] = -1
    my ($id, $dd, $ff, $t, $td, $p, $slp, $rh, $prec) = ("", -1, -1, 100, 100, -1, -1, -1, -1);
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
    $p = $report{'QNH'}{'hPa'} if (exists($report{'QNH'}{'hPa'}));
    $slp = $report{'SLPhPa'}{'hPa'} if (exists($report{'SLPhPa'}{'hPa'}));
    #if ($report{'precipInd'}{'s'} ne '/' && $report{'precipInd'}{'s'} == 2 && exists($report{'section3'})) {
    #    my ($prec_sec, %prec_info, %prec_now);
    #    for $prec_sec (@{$report{'section3'}}) {
    #        %prec_now = %$prec_sec;
    #        if (exists($prec_now{'precipHourly'})) {
    #            %prec_info = %prec_now;
    #        }
    #    }
    #    $prec = $prec_info{'precipHourly'}{'precipAmount'}{'v'} if (exists($prec_info{'precipHourly'}{'precipAmount'}));
    #}
    #elsif ($report{'precipInd'}{'s'} ne '/' && ($report{'precipInd'}{'s'} == 0 || $report{'precipInd'}{'s'} == 1)) {
    #    $prec = $report{'precipHourly'}{'precipAmount'}{'v'} if (exists($report{'precipHourly'}{'precipAmount'}));
    #}
    #printf STDERR "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2,%.2f\n", $id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp,$prec;
    return ($id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp,$prec);
}