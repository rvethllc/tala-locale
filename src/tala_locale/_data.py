# Phone-prefix (E.164 country code, digits only) -> (ISO-3166-1 alpha-2, ISO-4217, ISO-639-1)
#
# Ordering note: longer prefixes must come first when matching (e.g. "1868" for Trinidad
# before "1" for USA). The lookup in _core.py sorts by length descending.
#
# Currencies are ISO 4217. Language codes are ISO 639-1 two-letter codes.

PHONE_PREFIX_MAP: dict[str, tuple[str, str, str]] = {
    # --- West Africa ---
    "234": ("NG", "NGN", "en"),  # Nigeria
    "233": ("GH", "GHS", "en"),  # Ghana
    "221": ("SN", "XOF", "fr"),  # Senegal
    "225": ("CI", "XOF", "fr"),  # Côte d'Ivoire
    "226": ("BF", "XOF", "fr"),  # Burkina Faso
    "227": ("NE", "XOF", "fr"),  # Niger
    "228": ("TG", "XOF", "fr"),  # Togo
    "229": ("BJ", "XOF", "fr"),  # Benin
    "231": ("LR", "LRD", "en"),  # Liberia
    "232": ("SL", "SLL", "en"),  # Sierra Leone
    "220": ("GM", "GMD", "en"),  # Gambia
    "223": ("ML", "XOF", "fr"),  # Mali
    "224": ("GN", "GNF", "fr"),  # Guinea
    "245": ("GW", "XOF", "pt"),  # Guinea-Bissau
    "238": ("CV", "CVE", "pt"),  # Cape Verde
    "222": ("MR", "MRU", "ar"),  # Mauritania
    # --- East Africa ---
    "254": ("KE", "KES", "en"),  # Kenya
    "255": ("TZ", "TZS", "sw"),  # Tanzania
    "256": ("UG", "UGX", "en"),  # Uganda
    "250": ("RW", "RWF", "en"),  # Rwanda
    "257": ("BI", "BIF", "fr"),  # Burundi
    "251": ("ET", "ETB", "am"),  # Ethiopia
    "252": ("SO", "SOS", "so"),  # Somalia
    "253": ("DJ", "DJF", "fr"),  # Djibouti
    "291": ("ER", "ERN", "ti"),  # Eritrea
    "211": ("SS", "SSP", "en"),  # South Sudan
    # --- North Africa ---
    "20": ("EG", "EGP", "ar"),  # Egypt
    "212": ("MA", "MAD", "ar"),  # Morocco
    "213": ("DZ", "DZD", "ar"),  # Algeria
    "216": ("TN", "TND", "ar"),  # Tunisia
    "218": ("LY", "LYD", "ar"),  # Libya
    "249": ("SD", "SDG", "ar"),  # Sudan
    # --- Southern Africa ---
    "27": ("ZA", "ZAR", "en"),  # South Africa
    "260": ("ZM", "ZMW", "en"),  # Zambia
    "263": ("ZW", "ZWL", "en"),  # Zimbabwe
    "267": ("BW", "BWP", "en"),  # Botswana
    "266": ("LS", "LSL", "en"),  # Lesotho
    "268": ("SZ", "SZL", "en"),  # Eswatini
    "264": ("NA", "NAD", "en"),  # Namibia
    "265": ("MW", "MWK", "en"),  # Malawi
    "258": ("MZ", "MZN", "pt"),  # Mozambique
    # --- Central Africa ---
    "237": ("CM", "XAF", "fr"),  # Cameroon
    "236": ("CF", "XAF", "fr"),  # Central African Republic
    "235": ("TD", "XAF", "fr"),  # Chad
    "241": ("GA", "XAF", "fr"),  # Gabon
    "242": ("CG", "XAF", "fr"),  # Republic of the Congo
    "243": ("CD", "CDF", "fr"),  # DRC
    "244": ("AO", "AOA", "pt"),  # Angola
    "240": ("GQ", "XAF", "es"),  # Equatorial Guinea
    "239": ("ST", "STN", "pt"),  # São Tomé and Príncipe
    # --- Indian Ocean ---
    "261": ("MG", "MGA", "fr"),  # Madagascar
    "230": ("MU", "MUR", "en"),  # Mauritius
    "248": ("SC", "SCR", "en"),  # Seychelles
    "269": ("KM", "KMF", "ar"),  # Comoros
    # --- Western Europe ---
    "44": ("GB", "GBP", "en"),  # United Kingdom
    "33": ("FR", "EUR", "fr"),  # France
    "49": ("DE", "EUR", "de"),  # Germany
    "31": ("NL", "EUR", "nl"),  # Netherlands
    "34": ("ES", "EUR", "es"),  # Spain
    "39": ("IT", "EUR", "it"),  # Italy
    "41": ("CH", "CHF", "de"),  # Switzerland
    "43": ("AT", "EUR", "de"),  # Austria
    "32": ("BE", "EUR", "nl"),  # Belgium
    "351": ("PT", "EUR", "pt"),  # Portugal
    "353": ("IE", "EUR", "en"),  # Ireland
    "352": ("LU", "EUR", "fr"),  # Luxembourg
    "376": ("AD", "EUR", "ca"),  # Andorra
    "377": ("MC", "EUR", "fr"),  # Monaco
    "378": ("SM", "EUR", "it"),  # San Marino
    "379": ("VA", "EUR", "it"),  # Vatican
    "423": ("LI", "CHF", "de"),  # Liechtenstein
    # --- Northern Europe ---
    "46": ("SE", "SEK", "sv"),  # Sweden
    "47": ("NO", "NOK", "no"),  # Norway
    "45": ("DK", "DKK", "da"),  # Denmark
    "358": ("FI", "EUR", "fi"),  # Finland
    "354": ("IS", "ISK", "is"),  # Iceland
    "298": ("FO", "DKK", "fo"),  # Faroe Islands
    "299": ("GL", "DKK", "kl"),  # Greenland
    # --- Southern Europe ---
    "30": ("GR", "EUR", "el"),  # Greece
    "357": ("CY", "EUR", "el"),  # Cyprus
    "356": ("MT", "EUR", "mt"),  # Malta
    # --- Eastern Europe ---
    "7": ("RU", "RUB", "ru"),  # Russia (also covers +7 Kazakhstan — Russia wins on overlap)
    "380": ("UA", "UAH", "uk"),  # Ukraine
    "48": ("PL", "PLN", "pl"),  # Poland
    "36": ("HU", "HUF", "hu"),  # Hungary
    "420": ("CZ", "CZK", "cs"),  # Czech Republic
    "421": ("SK", "EUR", "sk"),  # Slovakia
    "40": ("RO", "RON", "ro"),  # Romania
    "359": ("BG", "BGN", "bg"),  # Bulgaria
    "370": ("LT", "EUR", "lt"),  # Lithuania
    "371": ("LV", "EUR", "lv"),  # Latvia
    "372": ("EE", "EUR", "et"),  # Estonia
    "375": ("BY", "BYN", "be"),  # Belarus
    "373": ("MD", "MDL", "ro"),  # Moldova
    "386": ("SI", "EUR", "sl"),  # Slovenia
    "385": ("HR", "EUR", "hr"),  # Croatia
    "387": ("BA", "BAM", "bs"),  # Bosnia and Herzegovina
    "381": ("RS", "RSD", "sr"),  # Serbia
    "382": ("ME", "EUR", "sr"),  # Montenegro
    "383": ("XK", "EUR", "sq"),  # Kosovo
    "389": ("MK", "MKD", "mk"),  # North Macedonia
    "355": ("AL", "ALL", "sq"),  # Albania
    # --- North America ---
    "1": ("US", "USD", "en"),  # USA (covers Canada — users can set CAD explicitly)
    "52": ("MX", "MXN", "es"),  # Mexico
    # --- Caribbean ---
    "1868": ("TT", "TTD", "en"),  # Trinidad and Tobago
    "1876": ("JM", "JMD", "en"),  # Jamaica
    "1246": ("BB", "BBD", "en"),  # Barbados
    "1784": ("VC", "XCD", "en"),  # Saint Vincent
    "1758": ("LC", "XCD", "en"),  # Saint Lucia
    "1473": ("GD", "XCD", "en"),  # Grenada
    "1767": ("DM", "XCD", "en"),  # Dominica
    "1268": ("AG", "XCD", "en"),  # Antigua and Barbuda
    "1869": ("KN", "XCD", "en"),  # Saint Kitts and Nevis
    "1809": ("DO", "DOP", "es"),  # Dominican Republic
    "509": ("HT", "HTG", "fr"),  # Haiti
    "53": ("CU", "CUP", "es"),  # Cuba
    # --- Central America ---
    "505": ("NI", "NIO", "es"),  # Nicaragua
    "503": ("SV", "USD", "es"),  # El Salvador
    "502": ("GT", "GTQ", "es"),  # Guatemala
    "504": ("HN", "HNL", "es"),  # Honduras
    "506": ("CR", "CRC", "es"),  # Costa Rica
    "507": ("PA", "PAB", "es"),  # Panama
    # --- South America ---
    "55": ("BR", "BRL", "pt"),  # Brazil
    "54": ("AR", "ARS", "es"),  # Argentina
    "56": ("CL", "CLP", "es"),  # Chile
    "57": ("CO", "COP", "es"),  # Colombia
    "51": ("PE", "PEN", "es"),  # Peru
    "58": ("VE", "VES", "es"),  # Venezuela
    "593": ("EC", "USD", "es"),  # Ecuador
    "591": ("BO", "BOB", "es"),  # Bolivia
    "595": ("PY", "PYG", "es"),  # Paraguay
    "598": ("UY", "UYU", "es"),  # Uruguay
    # --- Middle East ---
    "971": ("AE", "AED", "ar"),  # UAE
    "966": ("SA", "SAR", "ar"),  # Saudi Arabia
    "968": ("OM", "OMR", "ar"),  # Oman
    "974": ("QA", "QAR", "ar"),  # Qatar
    "973": ("BH", "BHD", "ar"),  # Bahrain
    "967": ("YE", "YER", "ar"),  # Yemen
    "965": ("KW", "KWD", "ar"),  # Kuwait
    "962": ("JO", "JOD", "ar"),  # Jordan
    "961": ("LB", "LBP", "ar"),  # Lebanon
    "963": ("SY", "SYP", "ar"),  # Syria
    "972": ("IL", "ILS", "he"),  # Israel / Palestine
    "964": ("IQ", "IQD", "ar"),  # Iraq
    "98": ("IR", "IRR", "fa"),  # Iran
    "90": ("TR", "TRY", "tr"),  # Turkey
    # --- South Asia ---
    "91": ("IN", "INR", "en"),  # India
    "92": ("PK", "PKR", "ur"),  # Pakistan
    "880": ("BD", "BDT", "bn"),  # Bangladesh
    "94": ("LK", "LKR", "si"),  # Sri Lanka
    "977": ("NP", "NPR", "ne"),  # Nepal
    "93": ("AF", "AFN", "ps"),  # Afghanistan
    # --- East Asia ---
    "86": ("CN", "CNY", "zh"),  # China
    "81": ("JP", "JPY", "ja"),  # Japan
    "82": ("KR", "KRW", "ko"),  # South Korea
    "852": ("HK", "HKD", "zh"),  # Hong Kong
    "853": ("MO", "MOP", "zh"),  # Macao
    "886": ("TW", "TWD", "zh"),  # Taiwan
    "976": ("MN", "MNT", "mn"),  # Mongolia
    "850": ("KP", "KPW", "ko"),  # North Korea
    # --- Southeast Asia ---
    "65": ("SG", "SGD", "en"),  # Singapore
    "60": ("MY", "MYR", "ms"),  # Malaysia
    "66": ("TH", "THB", "th"),  # Thailand
    "62": ("ID", "IDR", "id"),  # Indonesia
    "63": ("PH", "PHP", "en"),  # Philippines
    "84": ("VN", "VND", "vi"),  # Vietnam
    "95": ("MM", "MMK", "my"),  # Myanmar
    "855": ("KH", "KHR", "km"),  # Cambodia
    "856": ("LA", "LAK", "lo"),  # Laos
    # --- Central Asia ---
    "993": ("TM", "TMT", "tk"),  # Turkmenistan
    "992": ("TJ", "TJS", "tg"),  # Tajikistan
    "996": ("KG", "KGS", "ky"),  # Kyrgyzstan
    "998": ("UZ", "UZS", "uz"),  # Uzbekistan
    "994": ("AZ", "AZN", "az"),  # Azerbaijan
    "374": ("AM", "AMD", "hy"),  # Armenia
    "995": ("GE", "GEL", "ka"),  # Georgia
    # --- Oceania ---
    "61": ("AU", "AUD", "en"),  # Australia
    "64": ("NZ", "NZD", "en"),  # New Zealand
    "675": ("PG", "PGK", "en"),  # Papua New Guinea
    "679": ("FJ", "FJD", "en"),  # Fiji
    "676": ("TO", "TOP", "en"),  # Tonga
    "685": ("WS", "WST", "sm"),  # Samoa
    "686": ("KI", "AUD", "en"),  # Kiribati
    "692": ("MH", "USD", "en"),  # Marshall Islands
    "691": ("FM", "USD", "en"),  # Micronesia
    "680": ("PW", "USD", "en"),  # Palau
    "677": ("SB", "SBD", "en"),  # Solomon Islands
    "678": ("VU", "VUV", "bi"),  # Vanuatu
    "674": ("NR", "AUD", "en"),  # Nauru
    "688": ("TV", "AUD", "en"),  # Tuvalu
    "690": ("TK", "NZD", "en"),  # Tokelau
}
