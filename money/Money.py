# -*- coding: utf-8 -*-
import exceptions
from decimal import Decimal

class Currency:
    code = "XXX"
    country = ""
    countries = []
    name = ""
    numeric = "999"
    exchange_rate = Decimal("1.0")
    def __init__(self, code="", numeric="999", name="", symbol=u"", decimals=2, countries=[]):
        self.code = code
        self.numeric = numeric
        self.name = name
        self.symbol = symbol
        self.decimals = decimals
        self.countries = countries

    def __repr__(self):
        return self.code
    def set_exchange_rate(self, rate):
        if not isinstance(rate, Decimal):
            rate = Decimal(str(rate))
        self.exchange_rate = rate

CURRENCY = {}
CURRENCY['XXX'] = Currency(code="XXX", numeric="999")
DEFAULT_CURRENCY = CURRENCY['XXX']

def set_default_currency(code="XXX"):
    global DEFAULT_CURRENCY
    DEFAULT_CURRENCY = CURRENCY[code]

class IncorrectMoneyInputError(exceptions.Exception):
    def __init__(self):
        return
    def __unicode__(self):
        return u"Incorrectly formatted monetary input"

class Money:
    amount = Decimal("0.0")
    currency = DEFAULT_CURRENCY
    def __init__ (self, amount=Decimal("0.0"), currency=None):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount or 0))
        self.amount = amount
        if not currency:
            self.currency = DEFAULT_CURRENCY
        else:
            if not isinstance(currency, Currency):
                currency = CURRENCY[str(currency).upper()]
            self.currency = currency

    def __unicode__(self):
        return unicode(self.amount)
    def __float__(self):
        return float(self.amount)
    def __repr__(self):
        return '%s %5.2f' % (self.currency, self.amount)
    def __pos__(self):
        return Money(amount=self.amount, currency=self.currency)
    def __neg__(self):
        return Money(amount=-self.amount, currency=self.currency)
    def __add__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(amount = self.amount + other.amount, currency = self.currency)
            else:
                s = self.convert_to_default()
                other = other.convert_to_default()
                return Money(amount = s.amount + other.amount, currency = DEFAULT_CURRENCY)
        else:
            return Money(amount = self.amount + Decimal(str(other)), currency = self.currency)
    def __sub__(self, other):
        if isinstance(other, Money):
            if self.currency == other.currency:
                return Money(amount = self.amount - other.amount, currency = self.currency)
            else:
                s = self.convert_to_default()
                other = other.convert_to_default()
                return Money(amount = s.amount - other.amount, currency = DEFAULT_CURRENCY)
        else:
            return Money(amount = self.amount - Decimal(str(other)), currency = self.currency)
    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError, 'can not multiply monetary quantities'
        else:
            return Money(amount = self.amount*Decimal(str(other)), currency = self.currency)
    def __div__(self, other):
        if isinstance(other, Money):
            assert self.currency == other.currency, 'currency mismatch'
            return self.amount / other.amount
        else:
            return self.amount / Decimal(str(other))
    def __rmod__(self, other):
        """
        Calculate percentage of an amount.  The left-hand side of the operator must be a numeric value.  E.g.:
        >>> money = Money.Money(200, "USD")
        >>> 5 % money
        USD 10.00
        """
        if isinstance(other, Money):
            raise TypeError, 'invalid monetary operation'
        else:
            return Money(amount = Decimal(str(other)) * self.amount / 100, currency = self.currency)
    def convert_to_default(self):
        return Money(amount = self.amount * self.currency.exchange_rate, currency=DEFAULT_CURRENCY)
    def convert_to(self, currency):
        """
        Convert from one currency to another.
        """
        return None # TODO  (How??)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rdiv__ = __div__

    #
    # Override comparison operators
    #
    def __eq__(self, other):
        if isinstance(other, Money):
            return (self.amount == other.amount) and (self.currency == other.currency)
        # Allow comparison to 0
        if (other == 0) and (self.amount == 0):
            return True
        return False

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    def __lt__(self, other):
        if isinstance(other, Money):
            if (self.currency == other.currency):
                return (self.amount < other.amount)
            else:
                raise TypeError, 'can not compare different currencies'
        else:
            return (self.amount < Decimal(str(other)))
    def __gt__(self, other):
        if isinstance(other, Money):
            if (self.currency == other.currency):
                return (self.amount > other.amount)
            else:
                raise TypeError, 'can not compare different currencies'
        else:
            return (self.amount > Decimal(str(other)))
    def __le__(self, other):
        return self < other or self == other
    def __ge__(self, other):
        return self > other or self == other

    #
    # Miscellaneous helper methods
    #

    def allocate(self, ratios):
        """
        Allocates a sum of money to several accounts.
        """
        total = sum(ratios)
        remainder = self.amount
        results = []
        for i in range(0, len(ratios)):
            results.append(Money(amount = self.amount * ratios[i] / total, currency = self.currency))
            remainder -= results[i].amount
        i = 0
        while i < remainder:
            results[i].amount += Decimal("0.01")
            i += 1
        return results

    def spell_out(self):
        """
        Spells out a monetary amount.  E.g. "Two-hundred and twenty-six dollars and seventeen cents."
        """
        pass # TODO

    def from_string(self, s):
        """
        Parses a properly formatted string and extracts the monetary value and currency
        """
        try:
            self.amount = Decimal(str(s).strip())
            self.currency = DEFAULT_CURRENCY
        except:
            try:
                s = s.strip()
                self.currency = CURRENCY[s[:3].upper()]
                self.amount = Decimal(s[3:].strip())
            except:
                raise IncorrectMoneyInputError

#
# Definitions of ISO 4217 Currencies
# Source: http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/currency_codes/currency_codes_list-1.htm
# Symbols: http://www.xe.com/symbols.php
#

CURRENCY['AED'] = Currency(code='AED', numeric='784', decimals=2, symbol=u'', name='UAE Dirham', countries=['UNITED ARAB EMIRATES'])
CURRENCY['AFN'] = Currency(code='AFN', numeric='971', decimals=2, symbol=u'', name='Afghani', countries=['AFGHANISTAN'])
CURRENCY['ALL'] = Currency(code='ALL', numeric='008', decimals=2, symbol=u'', name='Lek', countries=['ALBANIA'])
CURRENCY['AMD'] = Currency(code='AMD', numeric='051', decimals=2, symbol=u'', name='Armenian Dram', countries=['ARMENIA'])
CURRENCY['ANG'] = Currency(code='ANG', numeric='532', decimals=2, symbol=u'', name='Netherlands Antillian Guilder', countries=['NETHERLANDS ANTILLES'])
CURRENCY['AOA'] = Currency(code='AOA', numeric='973', decimals=2, symbol=u'', name='Kwanza', countries=['ANGOLA'])
CURRENCY['ARS'] = Currency(code='ARS', numeric='032', decimals=2, symbol=u'', name='Argentine Peso', countries=['ARGENTINA'])
CURRENCY['AUD'] = Currency(code='AUD', numeric='036', decimals=2, symbol=u'$', name='Australian Dollar', countries=['AUSTRALIA', 'CHRISTMAS ISLAND', 'COCOS (KEELING) ISLANDS', 'HEARD ISLAND AND MCDONALD ISLANDS', 'KIRIBATI', 'NAURU', 'NORFOLK ISLAND', 'TUVALU'])
CURRENCY['AWG'] = Currency(code='AWG', numeric='533', decimals=2, symbol=u'', name='Aruban Guilder', countries=['ARUBA'])
CURRENCY['AZN'] = Currency(code='AZN', numeric='944', decimals=2, symbol=u'', name='Azerbaijanian Manat', countries=['AZERBAIJAN'])
CURRENCY['BAM'] = Currency(code='BAM', numeric='977', decimals=2, symbol=u'', name='Convertible Marks', countries=['BOSNIA AND HERZEGOVINA'])
CURRENCY['BBD'] = Currency(code='BBD', numeric='052', decimals=2, symbol=u'', name='Barbados Dollar', countries=['BARBADOS'])
CURRENCY['BDT'] = Currency(code='BDT', numeric='050', decimals=2, symbol=u'', name='Taka', countries=['BANGLADESH'])
CURRENCY['BGN'] = Currency(code='BGN', numeric='975', decimals=2, symbol=u'', name='Bulgarian Lev', countries=['BULGARIA'])
CURRENCY['BHD'] = Currency(code='BHD', numeric='048', decimals=2, symbol=u'', name='Bahraini Dinar', countries=['BAHRAIN'])
CURRENCY['BIF'] = Currency(code='BIF', numeric='108', decimals=2, symbol=u'', name='Burundi Franc', countries=['BURUNDI'])
CURRENCY['BMD'] = Currency(code='BMD', numeric='060', decimals=2, symbol=u'', name='Bermudian Dollar', countries=['BERMUDA'])
CURRENCY['BND'] = Currency(code='BND', numeric='096', decimals=2, symbol=u'', name='Brunei Dollar', countries=['BRUNEI DARUSSALAM'])
CURRENCY['BRL'] = Currency(code='BRL', numeric='986', decimals=2, symbol=u'', name='Brazilian Real', countries=['BRAZIL'])
CURRENCY['BSD'] = Currency(code='BSD', numeric='044', decimals=2, symbol=u'', name='Bahamian Dollar', countries=['BAHAMAS'])
CURRENCY['BWP'] = Currency(code='BWP', numeric='072', decimals=2, symbol=u'', name='Pula', countries=['BOTSWANA'])
CURRENCY['BYR'] = Currency(code='BYR', numeric='974', decimals=2, symbol=u'', name='Belarussian Ruble', countries=['BELARUS'])
CURRENCY['BZD'] = Currency(code='BZD', numeric='084', decimals=2, symbol=u'', name='Belize Dollar', countries=['BELIZE'])
CURRENCY['CAD'] = Currency(code='CAD', numeric='124', decimals=2, symbol=u'$', name='Canadian Dollar', countries=['CANADA'])
CURRENCY['CHF'] = Currency(code='CHF', numeric='756', decimals=2, symbol=u'Fr.', name='Swiss Franc', countries=['LIECHTENSTEIN'])
CURRENCY['CNY'] = Currency(code='CNY', numeric='156', decimals=2, symbol=u'', name='Yuan Renminbi', countries=['CHINA'])
CURRENCY['CRC'] = Currency(code='CRC', numeric='188', decimals=2, symbol=u'', name='Costa Rican Colon', countries=['COSTA RICA'])
CURRENCY['CUP'] = Currency(code='CUP', numeric='192', decimals=2, symbol=u'', name='Cuban Peso', countries=['CUBA'])
CURRENCY['CVE'] = Currency(code='CVE', numeric='132', decimals=2, symbol=u'', name='Cape Verde Escudo', countries=['CAPE VERDE'])
CURRENCY['CZK'] = Currency(code='CZK', numeric='203', decimals=2, symbol=u'', name='Czech Koruna', countries=['CZECH REPUBLIC'])
CURRENCY['DJF'] = Currency(code='DJF', numeric='262', decimals=2, symbol=u'', name='Djibouti Franc', countries=['DJIBOUTI'])
CURRENCY['DKK'] = Currency(code='DKK', numeric='208', decimals=2, symbol=u'', name='Danish Krone', countries=['DENMARK', 'FAROE ISLANDS', 'GREENLAND'])
CURRENCY['DOP'] = Currency(code='DOP', numeric='214', decimals=2, symbol=u'', name='Dominican Peso', countries=['DOMINICAN REPUBLIC'])
CURRENCY['DZD'] = Currency(code='DZD', numeric='012', decimals=2, symbol=u'', name='Algerian Dinar', countries=['ALGERIA'])
CURRENCY['EEK'] = Currency(code='EEK', numeric='233', decimals=2, symbol=u'', name='Kroon', countries=['ESTONIA'])
CURRENCY['EGP'] = Currency(code='EGP', numeric='818', decimals=2, symbol=u'', name='Egyptian Pound', countries=['EGYPT'])
CURRENCY['ERN'] = Currency(code='ERN', numeric='232', decimals=2, symbol=u'', name='Nakfa', countries=['ERITREA'])
CURRENCY['ETB'] = Currency(code='ETB', numeric='230', decimals=2, symbol=u'', name='Ethiopian Birr', countries=['ETHIOPIA'])
CURRENCY['EUR'] = Currency(code='EUR', numeric='978', decimals=2, symbol=u'€', name='Euro', countries=['ANDORRA', 'AUSTRIA', 'BELGIUM', 'FINLAND', 'FRANCE', 'FRENCH GUIANA', 'FRENCH SOUTHERN TERRITORIES', 'GERMANY', 'GREECE', 'GUADELOUPE', 'IRELAND', 'ITALY', 'LUXEMBOURG', 'MARTINIQUE', 'MAYOTTE', 'MONACO', 'MONTENEGRO', 'NETHERLANDS', 'PORTUGAL', 'R.UNION', 'SAINT PIERRE AND MIQUELON', 'SAN MARINO', 'SLOVENIA', 'SPAIN'])
CURRENCY['FJD'] = Currency(code='FJD', numeric='242', decimals=2, symbol=u'', name='Fiji Dollar', countries=['FIJI'])
CURRENCY['FKP'] = Currency(code='FKP', numeric='238', decimals=2, symbol=u'', name='Falkland Islands Pound', countries=['FALKLAND ISLANDS (MALVINAS)'])
CURRENCY['GBP'] = Currency(code='GBP', numeric='826', decimals=2, symbol=u'£', name='Pound Sterling', countries=['UNITED KINGDOM'])
CURRENCY['GEL'] = Currency(code='GEL', numeric='981', decimals=2, symbol=u'', name='Lari', countries=['GEORGIA'])
CURRENCY['GHS'] = Currency(code='GHS', numeric='936', decimals=2, symbol=u'', name='Ghana Cedi', countries=['GHANA'])
CURRENCY['GIP'] = Currency(code='GIP', numeric='292', decimals=2, symbol=u'', name='Gibraltar Pound', countries=['GIBRALTAR'])
CURRENCY['GMD'] = Currency(code='GMD', numeric='270', decimals=2, symbol=u'', name='Dalasi', countries=['GAMBIA'])
CURRENCY['GNF'] = Currency(code='GNF', numeric='324', decimals=2, symbol=u'', name='Guinea Franc', countries=['GUINEA'])
CURRENCY['GTQ'] = Currency(code='GTQ', numeric='320', decimals=2, symbol=u'', name='Quetzal', countries=['GUATEMALA'])
CURRENCY['GYD'] = Currency(code='GYD', numeric='328', decimals=2, symbol=u'', name='Guyana Dollar', countries=['GUYANA'])
CURRENCY['HKD'] = Currency(code='HKD', numeric='344', decimals=2, symbol=u'', name='Hong Kong Dollar', countries=['HONG KONG'])
CURRENCY['HNL'] = Currency(code='HNL', numeric='340', decimals=2, symbol=u'', name='Lempira', countries=['HONDURAS'])
CURRENCY['HRK'] = Currency(code='HRK', numeric='191', decimals=2, symbol=u'', name='Croatian Kuna', countries=['CROATIA'])
CURRENCY['HUF'] = Currency(code='HUF', numeric='348', decimals=2, symbol=u'', name='Forint', countries=['HUNGARY'])
CURRENCY['IDR'] = Currency(code='IDR', numeric='360', decimals=2, symbol=u'', name='Rupiah', countries=['INDONESIA'])
CURRENCY['ILS'] = Currency(code='ILS', numeric='376', decimals=2, symbol=u'', name='New Israeli Sheqel', countries=['ISRAEL'])
CURRENCY['INR'] = Currency(code='INR', numeric='356', decimals=2, symbol=u'', name='Indian Rupee', countries=['INDIA'])
CURRENCY['IQD'] = Currency(code='IQD', numeric='368', decimals=2, symbol=u'', name='Iraqi Dinar', countries=['IRAQ'])
CURRENCY['IRR'] = Currency(code='IRR', numeric='364', decimals=2, symbol=u'', name='Iranian Rial', countries=['IRAN'])
CURRENCY['ISK'] = Currency(code='ISK', numeric='352', decimals=2, symbol=u'', name='Iceland Krona', countries=['ICELAND'])
CURRENCY['JMD'] = Currency(code='JMD', numeric='388', decimals=2, symbol=u'', name='Jamaican Dollar', countries=['JAMAICA'])
CURRENCY['JOD'] = Currency(code='JOD', numeric='400', decimals=2, symbol=u'', name='Jordanian Dinar', countries=['JORDAN'])
CURRENCY['JPY'] = Currency(code='JPY', numeric='392', decimals=0, symbol=u'¥', name='Yen', countries=['JAPAN'])
CURRENCY['KES'] = Currency(code='KES', numeric='404', decimals=2, symbol=u'', name='Kenyan Shilling', countries=['KENYA'])
CURRENCY['KGS'] = Currency(code='KGS', numeric='417', decimals=2, symbol=u'', name='Som', countries=['KYRGYZSTAN'])
CURRENCY['KHR'] = Currency(code='KHR', numeric='116', decimals=2, symbol=u'', name='Riel', countries=['CAMBODIA'])
CURRENCY['KMF'] = Currency(code='KMF', numeric='174', decimals=2, symbol=u'', name='Comoro Franc', countries=['COMOROS'])
CURRENCY['KPW'] = Currency(code='KPW', numeric='408', decimals=2, symbol=u'', name='North Korean Won', countries=['KOREA'])
CURRENCY['KRW'] = Currency(code='KRW', numeric='410', decimals=2, symbol=u'', name='Won', countries=['KOREA'])
CURRENCY['KWD'] = Currency(code='KWD', numeric='414', decimals=2, symbol=u'', name='Kuwaiti Dinar', countries=['KUWAIT'])
CURRENCY['KYD'] = Currency(code='KYD', numeric='136', decimals=2, symbol=u'', name='Cayman Islands Dollar', countries=['CAYMAN ISLANDS'])
CURRENCY['KZT'] = Currency(code='KZT', numeric='398', decimals=2, symbol=u'', name='Tenge', countries=['KAZAKHSTAN'])
CURRENCY['LAK'] = Currency(code='LAK', numeric='418', decimals=2, symbol=u'', name='Kip', countries=['LAO PEOPLES DEMOCRATIC REPUBLIC'])
CURRENCY['LBP'] = Currency(code='LBP', numeric='422', decimals=2, symbol=u'', name='Lebanese Pound', countries=['LEBANON'])
CURRENCY['LKR'] = Currency(code='LKR', numeric='144', decimals=2, symbol=u'', name='Sri Lanka Rupee', countries=['SRI LANKA'])
CURRENCY['LRD'] = Currency(code='LRD', numeric='430', decimals=2, symbol=u'', name='Liberian Dollar', countries=['LIBERIA'])
CURRENCY['LTL'] = Currency(code='LTL', numeric='440', decimals=2, symbol=u'', name='Lithuanian Litas', countries=['LITHUANIA'])
CURRENCY['LVL'] = Currency(code='LVL', numeric='428', decimals=2, symbol=u'', name='Latvian Lats', countries=['LATVIA'])
CURRENCY['LYD'] = Currency(code='LYD', numeric='434', decimals=2, symbol=u'', name='Libyan Dinar', countries=['LIBYAN ARAB JAMAHIRIYA'])
CURRENCY['MAD'] = Currency(code='MAD', numeric='504', decimals=2, symbol=u'', name='Moroccan Dirham', countries=['MOROCCO', 'WESTERN SAHARA'])
CURRENCY['MDL'] = Currency(code='MDL', numeric='498', decimals=2, symbol=u'', name='Moldovan Leu', countries=['MOLDOVA'])
CURRENCY['MGA'] = Currency(code='MGA', numeric='969', decimals=2, symbol=u'', name='Malagasy Ariary', countries=['MADAGASCAR'])
CURRENCY['MKD'] = Currency(code='MKD', numeric='807', decimals=2, symbol=u'', name='Denar', countries=['MACEDONIA'])
CURRENCY['MMK'] = Currency(code='MMK', numeric='104', decimals=2, symbol=u'', name='Kyat', countries=['MYANMAR'])
CURRENCY['MNT'] = Currency(code='MNT', numeric='496', decimals=2, symbol=u'', name='Tugrik', countries=['MONGOLIA'])
CURRENCY['MOP'] = Currency(code='MOP', numeric='446', decimals=2, symbol=u'', name='Pataca', countries=['MACAO'])
CURRENCY['MRO'] = Currency(code='MRO', numeric='478', decimals=2, symbol=u'', name='Ouguiya', countries=['MAURITANIA'])
CURRENCY['MUR'] = Currency(code='MUR', numeric='480', decimals=2, symbol=u'', name='Mauritius Rupee', countries=['MAURITIUS'])
CURRENCY['MVR'] = Currency(code='MVR', numeric='462', decimals=2, symbol=u'', name='Rufiyaa', countries=['MALDIVES'])
CURRENCY['MWK'] = Currency(code='MWK', numeric='454', decimals=2, symbol=u'', name='Kwacha', countries=['MALAWI'])
CURRENCY['MYR'] = Currency(code='MYR', numeric='458', decimals=2, symbol=u'', name='Malaysian Ringgit', countries=['MALAYSIA'])
CURRENCY['MZN'] = Currency(code='MZN', numeric='943', decimals=2, symbol=u'', name='Metical', countries=['MOZAMBIQUE'])
CURRENCY['NGN'] = Currency(code='NGN', numeric='566', decimals=2, symbol=u'', name='Naira', countries=['NIGERIA'])
CURRENCY['NIO'] = Currency(code='NIO', numeric='558', decimals=2, symbol=u'', name='Cordoba Oro', countries=['NICARAGUA'])
CURRENCY['NOK'] = Currency(code='NOK', numeric='578', decimals=2, symbol=u'', name='Norwegian Krone', countries=['BOUVET ISLAND', 'NORWAY', 'SVALBARD AND JAN MAYEN'])
CURRENCY['NPR'] = Currency(code='NPR', numeric='524', decimals=2, symbol=u'', name='Nepalese Rupee', countries=['NEPAL'])
CURRENCY['NZD'] = Currency(code='NZD', numeric='554', decimals=2, symbol=u'', name='New Zealand Dollar', countries=['COOK ISLANDS', 'NEW ZEALAND', 'NIUE', 'PITCAIRN', 'TOKELAU'])
CURRENCY['OMR'] = Currency(code='OMR', numeric='512', decimals=2, symbol=u'', name='Rial Omani', countries=['OMAN'])
CURRENCY['PEN'] = Currency(code='PEN', numeric='604', decimals=2, symbol=u'', name='Nuevo Sol', countries=['PERU'])
CURRENCY['PGK'] = Currency(code='PGK', numeric='598', decimals=2, symbol=u'', name='Kina', countries=['PAPUA NEW GUINEA'])
CURRENCY['PHP'] = Currency(code='PHP', numeric='608', decimals=2, symbol=u'', name='Philippine Peso', countries=['PHILIPPINES'])
CURRENCY['PKR'] = Currency(code='PKR', numeric='586', decimals=2, symbol=u'', name='Pakistan Rupee', countries=['PAKISTAN'])
CURRENCY['PLN'] = Currency(code='PLN', numeric='985', decimals=2, symbol=u'', name='Zloty', countries=['POLAND'])
CURRENCY['PYG'] = Currency(code='PYG', numeric='600', decimals=2, symbol=u'', name='Guarani', countries=['PARAGUAY'])
CURRENCY['QAR'] = Currency(code='QAR', numeric='634', decimals=2, symbol=u'', name='Qatari Rial', countries=['QATAR'])
CURRENCY['RON'] = Currency(code='RON', numeric='946', decimals=2, symbol=u'', name='New Leu', countries=['ROMANIA'])
CURRENCY['RSD'] = Currency(code='RSD', numeric='941', decimals=2, symbol=u'', name='Serbian Dinar', countries=['SERBIA'])
CURRENCY['RUB'] = Currency(code='RUB', numeric='643', decimals=2, symbol=u'руб', name='Russian Ruble', countries=['RUSSIAN FEDERATION'])
CURRENCY['RWF'] = Currency(code='RWF', numeric='646', decimals=2, symbol=u'', name='Rwanda Franc', countries=['RWANDA'])
CURRENCY['SAR'] = Currency(code='SAR', numeric='682', decimals=2, symbol=u'', name='Saudi Riyal', countries=['SAUDI ARABIA'])
CURRENCY['SBD'] = Currency(code='SBD', numeric='090', decimals=2, symbol=u'', name='Solomon Islands Dollar', countries=['SOLOMON ISLANDS'])
CURRENCY['SCR'] = Currency(code='SCR', numeric='690', decimals=2, symbol=u'', name='Seychelles Rupee', countries=['SEYCHELLES'])
CURRENCY['SDG'] = Currency(code='SDG', numeric='938', decimals=2, symbol=u'', name='Sudanese Pound', countries=['SUDAN'])
CURRENCY['SEK'] = Currency(code='SEK', numeric='752', decimals=2, symbol=u'', name='Swedish Krona', countries=['SWEDEN'])
CURRENCY['SGD'] = Currency(code='SGD', numeric='702', decimals=2, symbol=u'', name='Singapore Dollar', countries=['SINGAPORE'])
CURRENCY['SHP'] = Currency(code='SHP', numeric='654', decimals=2, symbol=u'', name='Saint Helena Pound', countries=['SAINT HELENA'])
CURRENCY['SKK'] = Currency(code='SKK', numeric='703', decimals=2, symbol=u'', name='Slovak Koruna', countries=['SLOVAKIA'])
CURRENCY['SLL'] = Currency(code='SLL', numeric='694', decimals=2, symbol=u'', name='Leone', countries=['SIERRA LEONE'])
CURRENCY['SOS'] = Currency(code='SOS', numeric='706', decimals=2, symbol=u'', name='Somali Shilling', countries=['SOMALIA'])
CURRENCY['SRD'] = Currency(code='SRD', numeric='968', decimals=2, symbol=u'', name='Surinam Dollar', countries=['SURINAME'])
CURRENCY['STD'] = Currency(code='STD', numeric='678', decimals=2, symbol=u'', name='Dobra', countries=['SAO TOME AND PRINCIPE'])
CURRENCY['SYP'] = Currency(code='SYP', numeric='760', decimals=2, symbol=u'', name='Syrian Pound', countries=['SYRIAN ARAB REPUBLIC'])
CURRENCY['SZL'] = Currency(code='SZL', numeric='748', decimals=2, symbol=u'', name='Lilangeni', countries=['SWAZILAND'])
CURRENCY['THB'] = Currency(code='THB', numeric='764', decimals=2, symbol=u'', name='Baht', countries=['THAILAND'])
CURRENCY['TJS'] = Currency(code='TJS', numeric='972', decimals=2, symbol=u'', name='Somoni', countries=['TAJIKISTAN'])
CURRENCY['TMM'] = Currency(code='TMM', numeric='795', decimals=2, symbol=u'', name='Manat', countries=['TURKMENISTAN'])
CURRENCY['TND'] = Currency(code='TND', numeric='788', decimals=2, symbol=u'', name='Tunisian Dinar', countries=['TUNISIA'])
CURRENCY['TOP'] = Currency(code='TOP', numeric='776', decimals=2, symbol=u'', name='Paanga', countries=['TONGA'])
CURRENCY['TRY'] = Currency(code='TRY', numeric='949', decimals=2, symbol=u'', name='New Turkish Lira', countries=['TURKEY'])
CURRENCY['TTD'] = Currency(code='TTD', numeric='780', decimals=2, symbol=u'', name='Trinidad and Tobago Dollar', countries=['TRINIDAD AND TOBAGO'])
CURRENCY['TWD'] = Currency(code='TWD', numeric='901', decimals=2, symbol=u'', name='New Taiwan Dollar', countries=['TAIWAN'])
CURRENCY['TZS'] = Currency(code='TZS', numeric='834', decimals=2, symbol=u'', name='Tanzanian Shilling', countries=['TANZANIA'])
CURRENCY['UAH'] = Currency(code='UAH', numeric='980', decimals=2, symbol=u'', name='Hryvnia', countries=['UKRAINE'])
CURRENCY['UGX'] = Currency(code='UGX', numeric='800', decimals=2, symbol=u'', name='Uganda Shilling', countries=['UGANDA'])
CURRENCY['USD'] = Currency(code='USD', numeric='840', decimals=2, symbol=u'$', name='US Dollar', countries=['AMERICAN SAMOA', 'BRITISH INDIAN OCEAN TERRITORY', 'ECUADOR', 'GUAM', 'MARSHALL ISLANDS', 'MICRONESIA', 'NORTHERN MARIANA ISLANDS', 'PALAU', 'PUERTO RICO', 'TIMOR-LESTE', 'TURKS AND CAICOS ISLANDS', 'UNITED STATES MINOR OUTLYING ISLANDS', 'VIRGIN ISLANDS (BRITISH)', 'VIRGIN ISLANDS (U.S.)'])
CURRENCY['UZS'] = Currency(code='UZS', numeric='860', decimals=2, symbol=u'', name='Uzbekistan Sum', countries=['UZBEKISTAN'])
CURRENCY['VEF'] = Currency(code='VEF', numeric='937', decimals=2, symbol=u'', name='Bolivar Fuerte', countries=['VENEZUELA'])
CURRENCY['VND'] = Currency(code='VND', numeric='704', decimals=2, symbol=u'', name='Dong', countries=['VIET NAM'])
CURRENCY['VUV'] = Currency(code='VUV', numeric='548', decimals=2, symbol=u'', name='Vatu', countries=['VANUATU'])
CURRENCY['WST'] = Currency(code='WST', numeric='882', decimals=2, symbol=u'', name='Tala', countries=['SAMOA'])
CURRENCY['XAG'] = Currency(code='XAG', numeric='961', decimals=2, symbol=u'', name='Silver', countries=[])
CURRENCY['XAU'] = Currency(code='XAU', numeric='959', decimals=2, symbol=u'', name='Gold', countries=[])
CURRENCY['XBA'] = Currency(code='XBA', numeric='955', decimals=2, symbol=u'', name='Bond Markets Units European Composite Unit (EURCO)', countries=[])
CURRENCY['XBB'] = Currency(code='XBB', numeric='956', decimals=2, symbol=u'', name='European Monetary Unit (E.M.U.-6)', countries=[])
CURRENCY['XBC'] = Currency(code='XBC', numeric='957', decimals=2, symbol=u'', name='European Unit of Account 9(E.U.A.-9)', countries=[])
CURRENCY['XBD'] = Currency(code='XBD', numeric='958', decimals=2, symbol=u'', name='European Unit of Account 17(E.U.A.-17)', countries=[])
CURRENCY['XCD'] = Currency(code='XCD', numeric='951', decimals=2, symbol=u'', name='East Caribbean Dollar', countries=['ANGUILLA', 'ANTIGUA AND BARBUDA', 'DOMINICA', 'GRENADA', 'MONTSERRAT', 'SAINT KITTS AND NEVIS', 'SAINT LUCIA', 'SAINT VINCENT AND THE GRENADINES'])
CURRENCY['XDR'] = Currency(code='XDR', numeric='960', decimals=2, symbol=u'', name='SDR', countries=['INTERNATIONAL MONETARY FUND (I.M.F)'])
CURRENCY['XFO'] = Currency(code='XFO', numeric='Nil', decimals=2, symbol=u'', name='Gold-Franc', countries=[])
CURRENCY['XFU'] = Currency(code='XFU', numeric='Nil', decimals=2, symbol=u'', name='UIC-Franc', countries=[])
CURRENCY['XPD'] = Currency(code='XPD', numeric='964', decimals=2, symbol=u'', name='Palladium', countries=[])
CURRENCY['XPF'] = Currency(code='XPF', numeric='953', decimals=2, symbol=u'', name='CFP Franc', countries=['FRENCH POLYNESIA', 'NEW CALEDONIA', 'WALLIS AND FUTUNA'])
CURRENCY['XPT'] = Currency(code='XPT', numeric='962', decimals=2, symbol=u'', name='Platinum', countries=[])
CURRENCY['XTS'] = Currency(code='XTS', numeric='963', decimals=2, symbol=u'', name='Codes specifically reserved for testing purposes', countries=[])
CURRENCY['XXX'] = Currency(code='XXX', numeric='999', decimals=2, symbol=u'', name='XXX', countries=[])
CURRENCY['YER'] = Currency(code='YER', numeric='886', decimals=2, symbol=u'', name='Yemeni Rial', countries=['YEMEN'])
CURRENCY['ZAR'] = Currency(code='ZAR', numeric='710', decimals=2, symbol=u'', name='Rand', countries=['SOUTH AFRICA'])
CURRENCY['ZMK'] = Currency(code='ZMK', numeric='894', decimals=2, symbol=u'', name='Kwacha', countries=['ZAMBIA'])
CURRENCY['ZWD'] = Currency(code='ZWD', numeric='716', decimals=2, symbol=u'', name='Zimbabwe Dollar', countries=['ZIMBABWE'])