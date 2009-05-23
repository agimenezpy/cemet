#!/usr/bin/perl -w
use strict;
BEGIN { unshift @INC,("/home/agimenez/metaf2xml/lib"); }
use metaf2xml::parser;

my %convert = ('KT' => 1.85200, "KPH" => 1, "MPS" => 3.6);

main(scalar(@ARGV), @ARGV);

sub main {
    my ($argc, @argv) = @_;
    if ($argc > 0) {
        my ($tipo) = ($argv[0]);
        while (<STDIN>) {
            my $linea = $_;
            my (@params, $func) = (undef, undef);
            if ($tipo eq "-s") {
                @params = (0, 1);
                $func = \&processSynop;
            }
            elsif ($tipo eq "-t") {
                @params = (1, 0);
                $func = \&processTaf;
            }
            elsif ($tipo eq "-m") {
                @params = (0, 0);
                $func = \&processMetar;
            }
            else {
                print "\0";
                exit 1;
            }
            $linea =~ s/NIL|=//g;
            my %report = metaf2xml::parser::parseReport($linea, @params);
            if (%report && !exists($report{"ERROR"})) {
                my $bindata = &$func(\%report);
                print $bindata;
            }
            else {
                print STDERR $report{"ERROR"} if !exists($report{"ERROR"});
            }
        }
    }
    else {
        print "\0";
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
    my ($id, $dd, $ff, $t, $td, $p, $slp, $rh) = (0, -1, -1, 100, 100, -1, -1, -1);
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
    #printf STDERR "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", $id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp;
    return pack("if7", $id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp);
}

sub processTaf {
    my ($r) = @_;
    return pack("i", 1);
}

sub processMetar {
    my ($r) = @_;
    # Valores Invalidos (sin datos) none
    # ID (OACI) = NNNN
    # DD [0, 360] = -1
    # FF [0, inf] = -1
    # T [-99.9, 99.9] = 100
    # TD [-99.9, 99.9] = 100
    # P [1000, 1999,9] = -1
    # SLP [1000, 1999,9] = -1
    # RH [0, 100] = -1
    my ($id, $dd, $ff, $t, $td, $p, $slp, $rh) = ("NNNN", -1, -1, 100, 100, -1, -1, -1);
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
    $slp = $report{'QNH'}{'hPa'} if (exists($report{'QNH'}{'hPa'}));
    #printf STDERR "%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", $id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp;
    return pack("a4f7", $id,$dd,$ff*$convert{$unit},$t,$td,$rh,$p,$slp);
}