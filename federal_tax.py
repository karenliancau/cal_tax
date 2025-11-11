"""
美国联邦税计算器
US Federal Tax Calculator

支持计算联邦个人所得税、FICA税、资本利得税、自雇税等
Tax Year: 2024
"""

from typing import Dict, List, Tuple, Optional
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum


class FilingStatus(Enum):
    """报税身份"""
    SINGLE = "single"                           # 单身
    MARRIED_JOINTLY = "married_jointly"         # 已婚联合报税
    MARRIED_SEPARATELY = "married_separately"   # 已婚分别报税
    HEAD_OF_HOUSEHOLD = "head_of_household"     # 户主


class FederalTaxCalculator:
    """美国联邦税计算器"""

    # 2024年联邦所得税税率表
    TAX_BRACKETS_2024 = {
        FilingStatus.SINGLE: [
            (11600, 0.10),      # $0 - $11,600: 10%
            (47150, 0.12),      # $11,601 - $47,150: 12%
            (100525, 0.22),     # $47,151 - $100,525: 22%
            (191950, 0.24),     # $100,526 - $191,950: 24%
            (243725, 0.32),     # $191,951 - $243,725: 32%
            (609350, 0.35),     # $243,726 - $609,350: 35%
            (float('inf'), 0.37) # $609,351+: 37%
        ],
        FilingStatus.MARRIED_JOINTLY: [
            (23200, 0.10),      # $0 - $23,200: 10%
            (94300, 0.12),      # $23,201 - $94,300: 12%
            (201050, 0.22),     # $94,301 - $201,050: 22%
            (383900, 0.24),     # $201,051 - $383,900: 24%
            (487450, 0.32),     # $383,901 - $487,450: 32%
            (731200, 0.35),     # $487,451 - $731,200: 35%
            (float('inf'), 0.37) # $731,201+: 37%
        ],
        FilingStatus.MARRIED_SEPARATELY: [
            (11600, 0.10),
            (47150, 0.12),
            (100525, 0.22),
            (191950, 0.24),
            (243725, 0.32),
            (365600, 0.35),
            (float('inf'), 0.37)
        ],
        FilingStatus.HEAD_OF_HOUSEHOLD: [
            (16550, 0.10),
            (63100, 0.12),
            (100500, 0.22),
            (191950, 0.24),
            (243700, 0.32),
            (609350, 0.35),
            (float('inf'), 0.37)
        ]
    }

    # 2024年标准扣除额
    STANDARD_DEDUCTION_2024 = {
        FilingStatus.SINGLE: 14600,
        FilingStatus.MARRIED_JOINTLY: 29200,
        FilingStatus.MARRIED_SEPARATELY: 14600,
        FilingStatus.HEAD_OF_HOUSEHOLD: 21900
    }

    # FICA税率（社会保险税）
    SOCIAL_SECURITY_RATE = 0.062        # 6.2%
    SOCIAL_SECURITY_WAGE_BASE = 168600  # 2024年工资基数上限
    MEDICARE_RATE = 0.0145              # 1.45%
    ADDITIONAL_MEDICARE_RATE = 0.009    # 0.9% (高收入附加税)

    # 附加医疗保险税起征点
    ADDITIONAL_MEDICARE_THRESHOLD = {
        FilingStatus.SINGLE: 200000,
        FilingStatus.MARRIED_JOINTLY: 250000,
        FilingStatus.MARRIED_SEPARATELY: 125000,
        FilingStatus.HEAD_OF_HOUSEHOLD: 200000
    }

    # 自雇税率
    SELF_EMPLOYMENT_TAX_RATE = 0.153    # 15.3% (12.4% SS + 2.9% Medicare)
    SELF_EMPLOYMENT_DEDUCTION = 0.9235  # 可以扣除92.35%的净收入

    # 长期资本利得税率表
    LONG_TERM_CAPITAL_GAINS_RATES = {
        FilingStatus.SINGLE: [
            (47025, 0.0),       # $0 - $47,025: 0%
            (518900, 0.15),     # $47,026 - $518,900: 15%
            (float('inf'), 0.20) # $518,901+: 20%
        ],
        FilingStatus.MARRIED_JOINTLY: [
            (94050, 0.0),
            (583750, 0.15),
            (float('inf'), 0.20)
        ],
        FilingStatus.MARRIED_SEPARATELY: [
            (47025, 0.0),
            (291850, 0.15),
            (float('inf'), 0.20)
        ],
        FilingStatus.HEAD_OF_HOUSEHOLD: [
            (63000, 0.0),
            (551350, 0.15),
            (float('inf'), 0.20)
        ]
    }

    # 净投资收入税（NIIT）
    NET_INVESTMENT_INCOME_TAX_RATE = 0.038  # 3.8%
    NIIT_THRESHOLD = {
        FilingStatus.SINGLE: 200000,
        FilingStatus.MARRIED_JOINTLY: 250000,
        FilingStatus.MARRIED_SEPARATELY: 125000,
        FilingStatus.HEAD_OF_HOUSEHOLD: 200000
    }

    def __init__(self, tax_year: int = 2024):
        """初始化联邦税计算器"""
        self.tax_year = tax_year

    def calculate_income_tax(
        self,
        taxable_income: float,
        filing_status: FilingStatus
    ) -> Dict:
        """
        计算联邦所得税

        Args:
            taxable_income: 应税收入
            filing_status: 报税身份

        Returns:
            包含税额和详细信息的字典
        """
        income = Decimal(str(taxable_income))
        brackets = self.TAX_BRACKETS_2024[filing_status]

        total_tax = Decimal('0')
        previous_bracket = Decimal('0')
        bracket_details = []

        for bracket_limit, rate in brackets:
            bracket_limit_decimal = Decimal(str(bracket_limit))

            if income <= previous_bracket:
                break

            # 计算此税级的应税收入
            taxable_in_bracket = min(income, bracket_limit_decimal) - previous_bracket

            if taxable_in_bracket > 0:
                tax_in_bracket = taxable_in_bracket * Decimal(str(rate))
                total_tax += tax_in_bracket

                bracket_details.append({
                    "bracket_range": f"${previous_bracket:,.0f} - ${min(income, bracket_limit_decimal):,.0f}",
                    "rate": rate,
                    "taxable_amount": float(taxable_in_bracket),
                    "tax_amount": float(tax_in_bracket)
                })

            previous_bracket = bracket_limit_decimal

            if income <= bracket_limit_decimal:
                break

        total_tax = total_tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        effective_rate = (total_tax / income * 100) if income > 0 else Decimal('0')

        return {
            "taxable_income": float(income),
            "filing_status": filing_status.value,
            "total_tax": float(total_tax),
            "effective_rate": float(effective_rate),
            "bracket_details": bracket_details
        }

    def calculate_fica_tax(
        self,
        wages: float,
        filing_status: FilingStatus
    ) -> Dict:
        """
        计算FICA税（社会保险税和医疗保险税）

        Args:
            wages: 工资收入
            filing_status: 报税身份

        Returns:
            包含FICA税详情的字典
        """
        wages_decimal = Decimal(str(wages))

        # 社会保险税（有上限）
        ss_taxable = min(wages_decimal, Decimal(str(self.SOCIAL_SECURITY_WAGE_BASE)))
        social_security_tax = ss_taxable * Decimal(str(self.SOCIAL_SECURITY_RATE))

        # 医疗保险税（无上限）
        medicare_tax = wages_decimal * Decimal(str(self.MEDICARE_RATE))

        # 附加医疗保险税（高收入）
        additional_medicare_tax = Decimal('0')
        threshold = self.ADDITIONAL_MEDICARE_THRESHOLD[filing_status]
        if wages > threshold:
            additional_taxable = wages_decimal - Decimal(str(threshold))
            additional_medicare_tax = additional_taxable * Decimal(str(self.ADDITIONAL_MEDICARE_RATE))

        total_fica = social_security_tax + medicare_tax + additional_medicare_tax

        return {
            "wages": float(wages_decimal),
            "social_security_tax": float(social_security_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "medicare_tax": float(medicare_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "additional_medicare_tax": float(additional_medicare_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "total_fica_tax": float(total_fica.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "ss_wage_base": self.SOCIAL_SECURITY_WAGE_BASE
        }

    def calculate_self_employment_tax(
        self,
        net_earnings: float
    ) -> Dict:
        """
        计算自雇税

        Args:
            net_earnings: 净收入

        Returns:
            包含自雇税详情的字典
        """
        net_decimal = Decimal(str(net_earnings))

        # 计算92.35%的净收入作为自雇税基数
        se_taxable = net_decimal * Decimal(str(self.SELF_EMPLOYMENT_DEDUCTION))

        # 社会保险部分（有上限）
        ss_taxable = min(se_taxable, Decimal(str(self.SOCIAL_SECURITY_WAGE_BASE)))
        ss_tax = ss_taxable * Decimal(str(self.SOCIAL_SECURITY_RATE * 2))  # 雇主+雇员部分

        # 医疗保险部分（无上限）
        medicare_tax = se_taxable * Decimal(str(self.MEDICARE_RATE * 2))

        total_se_tax = ss_tax + medicare_tax

        # 可以扣除50%的自雇税
        deductible_se_tax = total_se_tax * Decimal('0.5')

        return {
            "net_earnings": float(net_decimal),
            "taxable_earnings": float(se_taxable),
            "social_security_tax": float(ss_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "medicare_tax": float(medicare_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "total_se_tax": float(total_se_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "deductible_amount": float(deductible_se_tax.quantize(Decimal('0.01'), ROUND_HALF_UP))
        }

    def calculate_capital_gains_tax(
        self,
        capital_gains: float,
        ordinary_income: float,
        filing_status: FilingStatus,
        holding_period: str = "long"  # "long" or "short"
    ) -> Dict:
        """
        计算资本利得税

        Args:
            capital_gains: 资本利得
            ordinary_income: 普通收入
            filing_status: 报税身份
            holding_period: 持有期限（"long"长期 > 1年，"short"短期 <= 1年）

        Returns:
            包含资本利得税详情的字典
        """
        gains = Decimal(str(capital_gains))
        ordinary = Decimal(str(ordinary_income))

        if holding_period == "short":
            # 短期资本利得按普通所得税率计税
            total_income = ordinary + gains
            tax_result = self.calculate_income_tax(float(total_income), filing_status)
            ordinary_tax_result = self.calculate_income_tax(float(ordinary), filing_status)

            cg_tax = Decimal(str(tax_result['total_tax'])) - Decimal(str(ordinary_tax_result['total_tax']))

            return {
                "capital_gains": float(gains),
                "holding_period": "short-term (≤ 1 year)",
                "tax_rate": "ordinary income rates",
                "capital_gains_tax": float(cg_tax.quantize(Decimal('0.01'), ROUND_HALF_UP))
            }
        else:
            # 长期资本利得
            rates = self.LONG_TERM_CAPITAL_GAINS_RATES[filing_status]

            # 使用普通收入+资本利得来确定税级
            total_income = ordinary + gains

            tax = Decimal('0')
            previous_bracket = Decimal('0')
            remaining_gains = gains
            applicable_rate = 0

            for bracket_limit, rate in rates:
                if remaining_gains <= 0:
                    break

                bracket_decimal = Decimal(str(bracket_limit))

                # 计算此税级中的资本利得
                income_in_bracket = min(total_income, bracket_decimal) - max(ordinary, previous_bracket)

                if income_in_bracket > 0:
                    taxable = min(income_in_bracket, remaining_gains)
                    tax += taxable * Decimal(str(rate))
                    remaining_gains -= taxable
                    applicable_rate = rate

                previous_bracket = bracket_decimal

            # 净投资收入税（NIIT）
            niit = Decimal('0')
            niit_threshold = self.NIIT_THRESHOLD[filing_status]
            if total_income > niit_threshold:
                niit_base = min(gains, total_income - Decimal(str(niit_threshold)))
                niit = niit_base * Decimal(str(self.NET_INVESTMENT_INCOME_TAX_RATE))

            total_cg_tax = tax + niit

            return {
                "capital_gains": float(gains),
                "holding_period": "long-term (> 1 year)",
                "primary_tax_rate": applicable_rate,
                "capital_gains_tax": float(tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
                "net_investment_income_tax": float(niit.quantize(Decimal('0.01'), ROUND_HALF_UP)),
                "total_tax": float(total_cg_tax.quantize(Decimal('0.01'), ROUND_HALF_UP))
            }

    def calculate_standard_deduction(
        self,
        filing_status: FilingStatus,
        age_65_or_older: int = 0,
        blind: int = 0
    ) -> Dict:
        """
        计算标准扣除额

        Args:
            filing_status: 报税身份
            age_65_or_older: 65岁或以上的人数
            blind: 盲人人数

        Returns:
            包含标准扣除额的字典
        """
        base_deduction = Decimal(str(self.STANDARD_DEDUCTION_2024[filing_status]))

        # 65岁以上或盲人的额外扣除
        additional_deduction = Decimal('0')
        if filing_status in [FilingStatus.SINGLE, FilingStatus.HEAD_OF_HOUSEHOLD]:
            additional_per_person = Decimal('1950')  # 2024年
        else:
            additional_per_person = Decimal('1550')  # 已婚

        total_additional = (age_65_or_older + blind) * additional_per_person
        additional_deduction = Decimal(str(total_additional))

        total_deduction = base_deduction + additional_deduction

        return {
            "filing_status": filing_status.value,
            "base_deduction": float(base_deduction),
            "additional_deduction": float(additional_deduction),
            "total_standard_deduction": float(total_deduction)
        }

    def calculate_total_tax_liability(
        self,
        gross_income: float,
        filing_status: FilingStatus,
        itemized_deductions: float = 0,
        tax_credits: float = 0,
        capital_gains: float = 0,
        self_employed: bool = False
    ) -> Dict:
        """
        计算总税负（综合计算）

        Args:
            gross_income: 总收入
            filing_status: 报税身份
            itemized_deductions: 分项扣除额
            tax_credits: 税收抵免
            capital_gains: 资本利得
            self_employed: 是否自雇

        Returns:
            完整的税务计算结果
        """
        gross = Decimal(str(gross_income))

        # 计算调整后总收入（AGI）
        agi = gross
        agi_adjustments = []

        # 如果是自雇，计算并扣除50%自雇税
        se_tax_deduction = Decimal('0')
        if self_employed:
            se_result = self.calculate_self_employment_tax(float(gross))
            se_tax_deduction = Decimal(str(se_result['deductible_amount']))
            agi -= se_tax_deduction
            agi_adjustments.append({
                "description": "Self-employment tax deduction",
                "amount": float(se_tax_deduction)
            })

        # 确定扣除额（标准扣除 vs 分项扣除）
        standard_ded = self.calculate_standard_deduction(filing_status)
        standard_deduction = Decimal(str(standard_ded['total_standard_deduction']))
        itemized = Decimal(str(itemized_deductions))

        deduction = max(standard_deduction, itemized)
        using_standard = deduction == standard_deduction

        # 计算应税收入
        taxable_income = max(agi - deduction, Decimal('0'))

        # 计算所得税
        income_tax_result = self.calculate_income_tax(float(taxable_income), filing_status)
        income_tax = Decimal(str(income_tax_result['total_tax']))

        # 计算资本利得税
        cg_tax = Decimal('0')
        if capital_gains > 0:
            cg_result = self.calculate_capital_gains_tax(
                capital_gains,
                float(taxable_income),
                filing_status,
                "long"
            )
            cg_tax = Decimal(str(cg_result['total_tax']))

        # 自雇税
        se_tax = Decimal('0')
        if self_employed:
            se_tax = Decimal(str(se_result['total_se_tax']))

        # 总税额（税前）
        total_tax_before_credits = income_tax + cg_tax + se_tax

        # 税收抵免
        credits = Decimal(str(tax_credits))

        # 最终税额
        final_tax = max(total_tax_before_credits - credits, Decimal('0'))

        return {
            "gross_income": float(gross),
            "agi_adjustments": agi_adjustments,
            "adjusted_gross_income": float(agi),
            "deduction_type": "Standard" if using_standard else "Itemized",
            "deduction_amount": float(deduction),
            "taxable_income": float(taxable_income),
            "income_tax": float(income_tax),
            "capital_gains_tax": float(cg_tax),
            "self_employment_tax": float(se_tax),
            "total_tax_before_credits": float(total_tax_before_credits),
            "tax_credits": float(credits),
            "total_tax_liability": float(final_tax.quantize(Decimal('0.01'), ROUND_HALF_UP)),
            "effective_tax_rate": float((final_tax / gross * 100) if gross > 0 else 0)
        }


def format_currency(amount: float) -> str:
    """格式化货币"""
    return f"${amount:,.2f}"


def format_percentage(rate: float) -> str:
    """格式化百分比"""
    return f"{rate:.2f}%"
