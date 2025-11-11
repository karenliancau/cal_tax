"""
田纳西州税务计算器
Tennessee Tax Calculator

支持计算田纳西州的销售税、房产税和企业税
"""

from typing import Dict, Optional
from decimal import Decimal, ROUND_HALF_UP


class TennesseeTaxCalculator:
    """田纳西州税务计算器主类"""

    # 田纳西州销售税率数据 (州税 7% + 地方税)
    SALES_TAX_RATES = {
        "Davidson": 0.0925,    # 纳什维尔 9.25%
        "Shelby": 0.0925,      # 孟菲斯 9.25%
        "Knox": 0.0925,        # 诺克斯维尔 9.25%
        "Hamilton": 0.0925,    # 查塔努加 9.25%
        "Rutherford": 0.0975,  # 9.75%
        "Williamson": 0.0975,  # 9.75%
        "Montgomery": 0.0975,  # 9.75%
        "Sumner": 0.0925,      # 9.25%
        "Madison": 0.0925,     # 9.25%
        "Bradley": 0.0925,     # 9.25%
        "default": 0.09,       # 默认约9%
    }

    # 房产税率 (每$100评估价值的税额)
    # 注：田纳西州房产按评估价值的25%计税
    PROPERTY_TAX_RATES = {
        "Davidson": 3.155,     # 每$100评估价值 $3.155
        "Shelby": 3.49,        # 每$100评估价值 $3.49
        "Knox": 2.47,          # 每$100评估价值 $2.47
        "Hamilton": 2.63,      # 每$100评估价值 $2.63
        "Rutherford": 2.48,    # 每$100评估价值 $2.48
        "Williamson": 2.69,    # 每$100评估价值 $2.69
        "default": 2.80,       # 默认税率
    }

    # 商业税税率 (按总收入的千分比)
    BUSINESS_TAX_RATES = {
        "retail": 0.0015,              # 零售 0.15%
        "wholesale": 0.0015,           # 批发 0.15%
        "manufacturing": 0.0015,       # 制造 0.15%
        "service": 0.0025,             # 服务 0.25%
        "financial": 0.0025,           # 金融 0.25%
        "professional": 0.00625,       # 专业服务 0.625%
        "default": 0.0025,             # 默认 0.25%
    }

    # 特许经营税 (Franchise Tax)
    FRANCHISE_TAX_RATE = 0.0025  # 0.25% of net worth
    FRANCHISE_TAX_MINIMUM = 100  # 最低$100

    def __init__(self):
        """初始化计算器"""
        pass

    def calculate_sales_tax(
        self,
        amount: float,
        county: str = "default",
        include_total: bool = True
    ) -> Dict[str, float]:
        """
        计算销售税

        Args:
            amount: 商品或服务金额
            county: 县名（如"Davidson", "Shelby"等）
            include_total: 是否返回含税总额

        Returns:
            包含税额和总额的字典
        """
        amount_decimal = Decimal(str(amount))

        # 获取该县的税率
        tax_rate = self.SALES_TAX_RATES.get(
            county,
            self.SALES_TAX_RATES["default"]
        )

        # 计算税额
        tax_amount = (amount_decimal * Decimal(str(tax_rate))).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        result = {
            "amount": float(amount_decimal),
            "tax_rate": tax_rate,
            "tax_amount": float(tax_amount),
            "county": county
        }

        if include_total:
            total = amount_decimal + tax_amount
            result["total"] = float(total)

        return result

    def calculate_property_tax(
        self,
        market_value: float,
        county: str = "default",
        assessment_ratio: float = 0.25
    ) -> Dict[str, float]:
        """
        计算房产税

        Args:
            market_value: 房产市场价值
            county: 县名
            assessment_ratio: 评估比例（田纳西州默认25%）

        Returns:
            包含税额和相关信息的字典
        """
        market_value_decimal = Decimal(str(market_value))

        # 计算评估价值
        assessed_value = market_value_decimal * Decimal(str(assessment_ratio))

        # 获取该县的税率
        tax_rate = self.PROPERTY_TAX_RATES.get(
            county,
            self.PROPERTY_TAX_RATES["default"]
        )

        # 计算税额：(评估价值 / 100) * 税率
        tax_amount = (assessed_value / Decimal('100')) * Decimal(str(tax_rate))
        tax_amount = tax_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return {
            "market_value": float(market_value_decimal),
            "assessed_value": float(assessed_value),
            "assessment_ratio": assessment_ratio,
            "tax_rate_per_100": tax_rate,
            "annual_tax": float(tax_amount),
            "county": county
        }

    def calculate_business_tax(
        self,
        gross_receipts: float,
        business_type: str = "default"
    ) -> Dict[str, float]:
        """
        计算商业税 (Business Tax)

        Args:
            gross_receipts: 总收入
            business_type: 企业类型

        Returns:
            包含税额的字典
        """
        gross_receipts_decimal = Decimal(str(gross_receipts))

        # 获取企业类型对应的税率
        tax_rate = self.BUSINESS_TAX_RATES.get(
            business_type.lower(),
            self.BUSINESS_TAX_RATES["default"]
        )

        # 计算税额
        tax_amount = (gross_receipts_decimal * Decimal(str(tax_rate))).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        return {
            "gross_receipts": float(gross_receipts_decimal),
            "business_type": business_type,
            "tax_rate": tax_rate,
            "tax_amount": float(tax_amount)
        }

    def calculate_franchise_tax(
        self,
        net_worth: float
    ) -> Dict[str, float]:
        """
        计算特许经营税 (Franchise Tax)

        Args:
            net_worth: 企业净资产

        Returns:
            包含税额的字典
        """
        net_worth_decimal = Decimal(str(net_worth))

        # 计算税额
        tax_amount = (net_worth_decimal * Decimal(str(self.FRANCHISE_TAX_RATE))).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        # 确保不低于最低税额
        if tax_amount < Decimal(str(self.FRANCHISE_TAX_MINIMUM)):
            tax_amount = Decimal(str(self.FRANCHISE_TAX_MINIMUM))

        return {
            "net_worth": float(net_worth_decimal),
            "tax_rate": self.FRANCHISE_TAX_RATE,
            "tax_amount": float(tax_amount),
            "minimum_tax": self.FRANCHISE_TAX_MINIMUM
        }

    def get_available_counties(self) -> list:
        """获取支持的县列表"""
        counties = [k for k in self.SALES_TAX_RATES.keys() if k != "default"]
        return sorted(counties)

    def get_available_business_types(self) -> list:
        """获取支持的企业类型列表"""
        types = [k for k in self.BUSINESS_TAX_RATES.keys() if k != "default"]
        return sorted(types)


def format_currency(amount: float) -> str:
    """格式化货币显示"""
    return f"${amount:,.2f}"


def format_percentage(rate: float) -> str:
    """格式化百分比显示"""
    return f"{rate * 100:.2f}%"
