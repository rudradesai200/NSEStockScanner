config = {

'GeneralConfig' : {
    "name": "BullishTargets_13_periods",
    "buy_threshold": 9,
    "sell_threshold": -4,
},

'IndicatorConfig' : {
    "requiredDataLength": 60,
    "field" : "close",
    "EMA": [13, 52],
    "SMA": [200],
    "RSI": 14,
    "BB": {'ma': 20, 'stddev': 2},
    "StochRSI": True,
    "MACD": {},
    "OBV": True
},

'EntryConfig' : {
	"conditions": [
		{"type":"rangePlus", "field1": "close", "field2": "SMA200", "period": 13, "color": 0, "score": 1},
		{"type":"rangePlus", "field1": "EMA52", "field2": "SMA200", "period": 13, "color": 0, "score": 1},
	],
    "indicators": [
        {"type":"lastCrossOver", "field1": "close", "field2": "52wh", "period": 13, "color": 3, "score": 6},
        {"type":"rangePlus", "field1": "RSI", "field2": 60, "period": 13, "color": 3, "score": 4},
        {"type":"rangePlus", "field1": "RSI", "field2": 60, "period": 52, "color": 3, "score": 8},
        {"type":"lastCrossOver", "field1": "EMA13", "field2": "EMA52", "period": 5, "color": 3, "score": 4},
        {"type":"lastCrossOver", "field1": "EMA52", "field2": "SMA200", "period": 5, "color": 3, "score": 8},
    ],
	"confirmations": [
		{"type":"lastCrossOver", "field1": "StochRSIFast", "field2": "StochRSISlow", "period": 5, "color": 1, "score": 2},
        # {"type":"rising", "field": "EMA13","period": 10, "color": 1, "score": 2},
        {"type":"rising", "field": "EMA13","period": 13, "color": 2, "score": 2},
        {"type":"rising", "field": "EMA13","period": 52, "color": 2, "score": 3},
        {"type":"rangeMinus", "field1": "BBNeck%", "field2": 10, "period": 1, "color": 1, "score": 2},
        {"type":"rangeMinus", "field1": "BBNeck%", "field2": 5, "period": 1, "color": 2, "score": 4},
	]
},

'ExitConfig' : {
	"conditions": [
		# {"type":"rangePlus", "field1": "close", "field2": "SMA200", "period": 13, "color": 0, "score": 1},
		# {"type":"rangeMinus", "field1": "RSI", "field2": 50, "period": 5, "color": 0, "score": 1},
        {"type":"falling","field":"close","period":5,"color": -3,"score":1},
	],
    "indicators": [
        # {"type":"lastCrossOver", "field1": "close", "field2": "52wl", "period": 13, "color": -3, "score": 8},
        {"type":"rangeMinus", "field1": "RSI", "field2": 40, "period": 13, "color": -2, "score": 4},
        {"type":"rangeMinus", "field1": "RSI", "field2": 40, "period": 52, "color": -3, "score": 8},
        {"type":"lastCrossOver", "field1": "EMA52", "field2": "EMA13", "period": 3, "color": -3, "score": 4},
        {"type":"lastCrossOver", "field1": "SMA200", "field2": "EMA52", "period": 3, "color": -3, "score": 8},
    ],
	"confirmations": [
        {"type":"hasMaxima","field":"macd_histogram","period":5,"color": -3,"score":4},
        {"type":"rangeMinus", "field1": "BBNeck%", "field2": 5, "period": 1, "color": -3, "score": 4},
		{"type":"lastCrossOver", "field1": "StochRSISlow", "field2": "StochRSIFast", "period": 5, "color": -1, "score": 2},
        {'type':'falling','field':'macd_histogram','period':3,"color": -2,'score':2},
        {'type':'falling','field':'obv','period':5, "color": -2,'score':3},
        {'type':'falling','field':'RSI','period':5, "color": -2, 'score':2},
        # {"type":"rising", "field": "EMA13","period": 10, "color": -1, "score": 2},
        {"type":"falling", "field": "EMA13","period": 13, "color": -2, "score": 2},
        {"type":"falling", "field": "EMA13","period": 52, "color": -2, "score": 3},
        {"type":"rangeMinus", "field1": "BBNeck%", "field2": 10, "period": 1, "color": -2, "score": 2},
	]
}
}