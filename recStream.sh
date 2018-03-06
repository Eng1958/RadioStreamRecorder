#!/bin/bash
# A litlle script is easier then the command line

## ./RadioStreamRecorder.py record wdr3 117 --recordingtime "22:04" --verbose --album "WDR3  Jazz - Differentiate the Hot from The Cool" --artist "Miles Davis Capitol Orchestra"
## ./RadioStreamRecorder.py record wdr3 116 --recordingtime "22:04" --verbose --album "WDR3 Jazz - Can You Jazz" --artist "Can" --splittime 15.0
## ./RadioStreamRecorder.py record wdr3 116 --recordingtime "20:04" --verbose --album "WDR3 Jazz - ScanJazz" --artist "V-Tolstoy_WDR-Bigband" --splittime 15.0
## ./RadioStreamRecorder.py record wdr3 116 --recordingtime "22:04" --verbose --album "WDR3 Jazz - Revolutionaer und Romantiker" --artist "Charlie Haden" --splittime 15.0
## ./RadioStreamRecorder.py record wdr3 116 --recordingtime "22:04" --verbose --album "WDR3 Jazz - Seelensaitenklaenge" --artist "Philip Catherine" --splittime 15.0
./RadioStreamRecorder/RadioStreamRecorder.py record DLF 5 --recordingtime "20:28" --verbose --album "DLF - Test" --artist "Various" --splittime 15.0
