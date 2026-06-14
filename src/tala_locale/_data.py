# Phone-prefix (E.164 country code, digits only) -> (ISO-3166-1 alpha-2, ISO-4217, BCP-47)
#
# Ordering note: longer prefixes must come first when matching (e.g. "1868" for Trinidad
# before "1" for USA). The lookup in _core.py sorts by length descending.
#
# Currencies are ISO 4217. Language codes are BCP 47 tags (e.g. "en-NG", "ar-EG").
# Primary language = the dominant/official language for that country in business contexts.
# For multi-language countries, see ExtendedLocale.languages in _extended_data.py.

PHONE_PREFIX_MAP: dict[str, tuple[str, str, str]] = {
    # --- West Africa ---
    "234": ("NG", "NGN", "en-NG"),  # Nigeria
    "233": ("GH", "GHS", "en-GH"),  # Ghana
    "221": ("SN", "XOF", "fr-SN"),  # Senegal
    "225": ("CI", "XOF", "fr-CI"),  # Côte d'Ivoire
    "226": ("BF", "XOF", "fr-BF"),  # Burkina Faso
    "227": ("NE", "XOF", "fr-NE"),  # Niger
    "228": ("TG", "XOF", "fr-TG"),  # Togo
    "229": ("BJ", "XOF", "fr-BJ"),  # Benin
    "231": ("LR", "LRD", "en-LR"),  # Liberia
    "232": ("SL", "SLL", "en-SL"),  # Sierra Leone
    "220": ("GM", "GMD", "en-GM"),  # Gambia
    "223": ("ML", "XOF", "fr-ML"),  # Mali
    "224": ("GN", "GNF", "fr-GN"),  # Guinea
    "245": ("GW", "XOF", "pt-GW"),  # Guinea-Bissau
    "238": ("CV", "CVE", "pt-CV"),  # Cape Verde
    "222": ("MR", "MRU", "ar-MR"),  # Mauritania
    # --- East Africa ---
    "254": ("KE", "KES", "sw-KE"),  # Kenya
    "255": ("TZ", "TZS", "sw-TZ"),  # Tanzania
    "256": ("UG", "UGX", "en-UG"),  # Uganda
    "250": ("RW", "RWF", "rw-RW"),  # Rwanda
    "257": ("BI", "BIF", "fr-BI"),  # Burundi
    "251": ("ET", "ETB", "am-ET"),  # Ethiopia
    "252": ("SO", "SOS", "so-SO"),  # Somalia
    "253": ("DJ", "DJF", "fr-DJ"),  # Djibouti
    "291": ("ER", "ERN", "ti-ER"),  # Eritrea
    "211": ("SS", "SSP", "en-SS"),  # South Sudan
    # --- North Africa ---
    "20": ("EG", "EGP", "ar-EG"),  # Egypt
    "212": ("MA", "MAD", "ar-MA"),  # Morocco
    "213": ("DZ", "DZD", "ar-DZ"),  # Algeria
    "216": ("TN", "TND", "ar-TN"),  # Tunisia
    "218": ("LY", "LYD", "ar-LY"),  # Libya
    "249": ("SD", "SDG", "ar-SD"),  # Sudan
    # --- Southern Africa ---
    "27": ("ZA", "ZAR", "en-ZA"),  # South Africa
    "260": ("ZM", "ZMW", "en-ZM"),  # Zambia
    "263": ("ZW", "ZWL", "en-ZW"),  # Zimbabwe
    "267": ("BW", "BWP", "en-BW"),  # Botswana
    "266": ("LS", "LSL", "en-LS"),  # Lesotho
    "268": ("SZ", "SZL", "en-SZ"),  # Eswatini
    "264": ("NA", "NAD", "en-NA"),  # Namibia
    "265": ("MW", "MWK", "en-MW"),  # Malawi
    "258": ("MZ", "MZN", "pt-MZ"),  # Mozambique
    # --- Central Africa ---
    "237": ("CM", "XAF", "fr-CM"),  # Cameroon
    "236": ("CF", "XAF", "fr-CF"),  # Central African Republic
    "235": ("TD", "XAF", "fr-TD"),  # Chad
    "241": ("GA", "XAF", "fr-GA"),  # Gabon
    "242": ("CG", "XAF", "fr-CG"),  # Republic of the Congo
    "243": ("CD", "CDF", "fr-CD"),  # DRC
    "244": ("AO", "AOA", "pt-AO"),  # Angola
    "240": ("GQ", "XAF", "es-GQ"),  # Equatorial Guinea
    "239": ("ST", "STN", "pt-ST"),  # São Tomé and Príncipe
    # --- Indian Ocean ---
    "261": ("MG", "MGA", "mg-MG"),  # Madagascar
    "230": ("MU", "MUR", "en-MU"),  # Mauritius
    "248": ("SC", "SCR", "en-SC"),  # Seychelles
    "269": ("KM", "KMF", "ar-KM"),  # Comoros
    # --- Western Europe ---
    "44": ("GB", "GBP", "en-GB"),  # United Kingdom
    "33": ("FR", "EUR", "fr-FR"),  # France
    "49": ("DE", "EUR", "de-DE"),  # Germany
    "31": ("NL", "EUR", "nl-NL"),  # Netherlands
    "34": ("ES", "EUR", "es-ES"),  # Spain
    "39": ("IT", "EUR", "it-IT"),  # Italy
    "41": ("CH", "CHF", "de-CH"),  # Switzerland
    "43": ("AT", "EUR", "de-AT"),  # Austria
    "32": ("BE", "EUR", "fr-BE"),  # Belgium
    "351": ("PT", "EUR", "pt-PT"),  # Portugal
    "353": ("IE", "EUR", "en-IE"),  # Ireland
    "352": ("LU", "EUR", "fr-LU"),  # Luxembourg
    "376": ("AD", "EUR", "ca-AD"),  # Andorra
    "377": ("MC", "EUR", "fr-MC"),  # Monaco
    "378": ("SM", "EUR", "it-SM"),  # San Marino
    "379": ("VA", "EUR", "it-VA"),  # Vatican
    "423": ("LI", "CHF", "de-LI"),  # Liechtenstein
    # --- Northern Europe ---
    "46": ("SE", "SEK", "sv-SE"),  # Sweden
    "47": ("NO", "NOK", "nb-NO"),  # Norway
    "45": ("DK", "DKK", "da-DK"),  # Denmark
    "358": ("FI", "EUR", "fi-FI"),  # Finland
    "354": ("IS", "ISK", "is-IS"),  # Iceland
    "298": ("FO", "DKK", "fo-FO"),  # Faroe Islands
    "299": ("GL", "DKK", "kl-GL"),  # Greenland
    # --- Southern Europe ---
    "30": ("GR", "EUR", "el-GR"),  # Greece
    "357": ("CY", "EUR", "el-CY"),  # Cyprus
    "356": ("MT", "EUR", "mt-MT"),  # Malta
    # --- Eastern Europe ---
    "7": ("RU", "RUB", "ru-RU"),  # Russia
    "380": ("UA", "UAH", "uk-UA"),  # Ukraine
    "48": ("PL", "PLN", "pl-PL"),  # Poland
    "36": ("HU", "HUF", "hu-HU"),  # Hungary
    "420": ("CZ", "CZK", "cs-CZ"),  # Czech Republic
    "421": ("SK", "EUR", "sk-SK"),  # Slovakia
    "40": ("RO", "RON", "ro-RO"),  # Romania
    "359": ("BG", "BGN", "bg-BG"),  # Bulgaria
    "370": ("LT", "EUR", "lt-LT"),  # Lithuania
    "371": ("LV", "EUR", "lv-LV"),  # Latvia
    "372": ("EE", "EUR", "et-EE"),  # Estonia
    "375": ("BY", "BYN", "be-BY"),  # Belarus
    "373": ("MD", "MDL", "ro-MD"),  # Moldova
    "386": ("SI", "EUR", "sl-SI"),  # Slovenia
    "385": ("HR", "EUR", "hr-HR"),  # Croatia
    "387": ("BA", "BAM", "bs-BA"),  # Bosnia and Herzegovina
    "381": ("RS", "RSD", "sr-RS"),  # Serbia
    "382": ("ME", "EUR", "sr-ME"),  # Montenegro
    "383": ("XK", "EUR", "sq-XK"),  # Kosovo
    "389": ("MK", "MKD", "mk-MK"),  # North Macedonia
    "355": ("AL", "ALL", "sq-AL"),  # Albania
    # --- North America ---
    "1": ("US", "USD", "en-US"),  # USA (covers Canada — area codes disambiguate)
    "52": ("MX", "MXN", "es-MX"),  # Mexico
    # --- Caribbean ---
    "1868": ("TT", "TTD", "en-TT"),  # Trinidad and Tobago
    "1876": ("JM", "JMD", "en-JM"),  # Jamaica
    "1246": ("BB", "BBD", "en-BB"),  # Barbados
    "1784": ("VC", "XCD", "en-VC"),  # Saint Vincent
    "1758": ("LC", "XCD", "en-LC"),  # Saint Lucia
    "1473": ("GD", "XCD", "en-GD"),  # Grenada
    "1767": ("DM", "XCD", "en-DM"),  # Dominica
    "1268": ("AG", "XCD", "en-AG"),  # Antigua and Barbuda
    "1869": ("KN", "XCD", "en-KN"),  # Saint Kitts and Nevis
    "1809": ("DO", "DOP", "es-DO"),  # Dominican Republic
    "509": ("HT", "HTG", "fr-HT"),  # Haiti
    "53": ("CU", "CUP", "es-CU"),  # Cuba
    # --- Central America ---
    "505": ("NI", "NIO", "es-NI"),  # Nicaragua
    "503": ("SV", "USD", "es-SV"),  # El Salvador
    "502": ("GT", "GTQ", "es-GT"),  # Guatemala
    "504": ("HN", "HNL", "es-HN"),  # Honduras
    "506": ("CR", "CRC", "es-CR"),  # Costa Rica
    "507": ("PA", "PAB", "es-PA"),  # Panama
    # --- South America ---
    "55": ("BR", "BRL", "pt-BR"),  # Brazil
    "54": ("AR", "ARS", "es-AR"),  # Argentina
    "56": ("CL", "CLP", "es-CL"),  # Chile
    "57": ("CO", "COP", "es-CO"),  # Colombia
    "51": ("PE", "PEN", "es-PE"),  # Peru
    "58": ("VE", "VES", "es-VE"),  # Venezuela
    "593": ("EC", "USD", "es-EC"),  # Ecuador
    "591": ("BO", "BOB", "es-BO"),  # Bolivia
    "595": ("PY", "PYG", "es-PY"),  # Paraguay
    "598": ("UY", "UYU", "es-UY"),  # Uruguay
    # --- Middle East ---
    "971": ("AE", "AED", "ar-AE"),  # UAE
    "966": ("SA", "SAR", "ar-SA"),  # Saudi Arabia
    "968": ("OM", "OMR", "ar-OM"),  # Oman
    "974": ("QA", "QAR", "ar-QA"),  # Qatar
    "973": ("BH", "BHD", "ar-BH"),  # Bahrain
    "967": ("YE", "YER", "ar-YE"),  # Yemen
    "965": ("KW", "KWD", "ar-KW"),  # Kuwait
    "962": ("JO", "JOD", "ar-JO"),  # Jordan
    "961": ("LB", "LBP", "ar-LB"),  # Lebanon
    "963": ("SY", "SYP", "ar-SY"),  # Syria
    "972": ("IL", "ILS", "he-IL"),  # Israel / Palestine
    "964": ("IQ", "IQD", "ar-IQ"),  # Iraq
    "98": ("IR", "IRR", "fa-IR"),  # Iran
    "90": ("TR", "TRY", "tr-TR"),  # Turkey
    # --- South Asia ---
    "91": ("IN", "INR", "en-IN"),  # India
    "92": ("PK", "PKR", "ur-PK"),  # Pakistan
    "880": ("BD", "BDT", "bn-BD"),  # Bangladesh
    "94": ("LK", "LKR", "si-LK"),  # Sri Lanka
    "977": ("NP", "NPR", "ne-NP"),  # Nepal
    "93": ("AF", "AFN", "ps-AF"),  # Afghanistan
    # --- East Asia ---
    "86": ("CN", "CNY", "zh-CN"),  # China
    "81": ("JP", "JPY", "ja-JP"),  # Japan
    "82": ("KR", "KRW", "ko-KR"),  # South Korea
    "852": ("HK", "HKD", "zh-HK"),  # Hong Kong
    "853": ("MO", "MOP", "zh-MO"),  # Macao
    "886": ("TW", "TWD", "zh-TW"),  # Taiwan
    "976": ("MN", "MNT", "mn-MN"),  # Mongolia
    "850": ("KP", "KPW", "ko-KP"),  # North Korea
    # --- Southeast Asia ---
    "65": ("SG", "SGD", "en-SG"),  # Singapore
    "60": ("MY", "MYR", "ms-MY"),  # Malaysia
    "66": ("TH", "THB", "th-TH"),  # Thailand
    "62": ("ID", "IDR", "id-ID"),  # Indonesia
    "63": ("PH", "PHP", "en-PH"),  # Philippines
    "84": ("VN", "VND", "vi-VN"),  # Vietnam
    "95": ("MM", "MMK", "my-MM"),  # Myanmar
    "855": ("KH", "KHR", "km-KH"),  # Cambodia
    "856": ("LA", "LAK", "lo-LA"),  # Laos
    # --- Central Asia ---
    "993": ("TM", "TMT", "tk-TM"),  # Turkmenistan
    "992": ("TJ", "TJS", "tg-TJ"),  # Tajikistan
    "996": ("KG", "KGS", "ky-KG"),  # Kyrgyzstan
    "998": ("UZ", "UZS", "uz-UZ"),  # Uzbekistan
    "994": ("AZ", "AZN", "az-AZ"),  # Azerbaijan
    "374": ("AM", "AMD", "hy-AM"),  # Armenia
    "995": ("GE", "GEL", "ka-GE"),  # Georgia
    # --- Oceania ---
    "61": ("AU", "AUD", "en-AU"),  # Australia
    "64": ("NZ", "NZD", "en-NZ"),  # New Zealand
    "675": ("PG", "PGK", "en-PG"),  # Papua New Guinea
    "679": ("FJ", "FJD", "en-FJ"),  # Fiji
    "676": ("TO", "TOP", "en-TO"),  # Tonga
    "685": ("WS", "WST", "sm-WS"),  # Samoa
    "686": ("KI", "AUD", "en-KI"),  # Kiribati
    "692": ("MH", "USD", "en-MH"),  # Marshall Islands
    "691": ("FM", "USD", "en-FM"),  # Micronesia
    "680": ("PW", "USD", "en-PW"),  # Palau
    "677": ("SB", "SBD", "en-SB"),  # Solomon Islands
    "678": ("VU", "VUV", "bi-VU"),  # Vanuatu
    "674": ("NR", "AUD", "en-NR"),  # Nauru
    "688": ("TV", "AUD", "en-TV"),  # Tuvalu
    "690": ("TK", "NZD", "en-TK"),  # Tokelau
}
