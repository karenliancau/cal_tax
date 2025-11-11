"""
田纳西州税务计算器使用示例
Tennessee Tax Calculator Usage Examples
"""

from tennessee_tax import TennesseeTaxCalculator, format_currency, format_percentage


def main():
    # 创建计算器实例
    calculator = TennesseeTaxCalculator()

    print("=" * 70)
    print("田纳西州税务计算器使用示例")
    print("Tennessee Tax Calculator Examples")
    print("=" * 70)

    # 示例1: 销售税计算
    print("\n【示例 1: 销售税计算】")
    print("-" * 70)
    purchase_amount = 1500.00
    county = "Davidson"

    sales_tax = calculator.calculate_sales_tax(purchase_amount, county)

    print(f"购买商品金额: {format_currency(sales_tax['amount'])}")
    print(f"地点: {sales_tax['county']} County")
    print(f"销售税率: {format_percentage(sales_tax['tax_rate'])}")
    print(f"销售税额: {format_currency(sales_tax['tax_amount'])}")
    print(f"总计: {format_currency(sales_tax['total'])}")

    # 示例2: 房产税计算
    print("\n【示例 2: 房产税计算】")
    print("-" * 70)
    home_value = 350000
    county = "Knox"

    property_tax = calculator.calculate_property_tax(home_value, county)

    print(f"房产市场价值: {format_currency(property_tax['market_value'])}")
    print(f"评估价值 (25%): {format_currency(property_tax['assessed_value'])}")
    print(f"地点: {property_tax['county']} County")
    print(f"税率: ${property_tax['tax_rate_per_100']:.2f} 每 $100 评估价值")
    print(f"年度房产税: {format_currency(property_tax['annual_tax'])}")
    print(f"月均房产税: {format_currency(property_tax['annual_tax'] / 12)}")

    # 示例3: 商业税计算
    print("\n【示例 3: 商业税计算】")
    print("-" * 70)
    annual_receipts = 750000
    business_type = "retail"

    business_tax = calculator.calculate_business_tax(annual_receipts, business_type)

    print(f"年度总收入: {format_currency(business_tax['gross_receipts'])}")
    print(f"企业类型: {business_tax['business_type']}")
    print(f"商业税率: {format_percentage(business_tax['tax_rate'])}")
    print(f"应缴商业税: {format_currency(business_tax['tax_amount'])}")

    # 示例4: 特许经营税计算
    print("\n【示例 4: 特许经营税计算】")
    print("-" * 70)
    company_net_worth = 2500000

    franchise_tax = calculator.calculate_franchise_tax(company_net_worth)

    print(f"企业净资产: {format_currency(franchise_tax['net_worth'])}")
    print(f"特许经营税率: {format_percentage(franchise_tax['tax_rate'])}")
    print(f"应缴特许经营税: {format_currency(franchise_tax['tax_amount'])}")

    # 示例5: 比较不同县的税率
    print("\n【示例 5: 不同县的销售税比较】")
    print("-" * 70)
    amount = 100.00
    counties_to_compare = ["Davidson", "Shelby", "Knox", "Rutherford"]

    print(f"商品金额: {format_currency(amount)}\n")
    for county in counties_to_compare:
        result = calculator.calculate_sales_tax(amount, county)
        print(f"{county:15s}: 税额 {format_currency(result['tax_amount'])}, "
              f"总计 {format_currency(result['total'])}")

    # 示例6: 不同企业类型的商业税比较
    print("\n【示例 6: 不同企业类型的商业税比较】")
    print("-" * 70)
    receipts = 500000
    business_types = calculator.get_available_business_types()

    print(f"年度收入: {format_currency(receipts)}\n")
    for btype in business_types:
        result = calculator.calculate_business_tax(receipts, btype)
        print(f"{btype:15s}: {format_currency(result['tax_amount'])} "
              f"({format_percentage(result['tax_rate'])})")

    # 示例7: 购房总成本估算（包含首年房产税）
    print("\n【示例 7: 购房总成本估算】")
    print("-" * 70)
    home_price = 400000
    county = "Williamson"

    # 假设首付20%
    down_payment = home_price * 0.20
    loan_amount = home_price - down_payment

    # 计算房产税
    prop_tax = calculator.calculate_property_tax(home_price, county)

    print(f"房屋售价: {format_currency(home_price)}")
    print(f"首付款 (20%): {format_currency(down_payment)}")
    print(f"贷款金额: {format_currency(loan_amount)}")
    print(f"首年房产税: {format_currency(prop_tax['annual_tax'])}")
    print(f"月均房产税: {format_currency(prop_tax['annual_tax'] / 12)}")

    print("\n" + "=" * 70)
    print("更多信息请访问: https://www.tn.gov/revenue")
    print("⚠️  以上计算结果仅供参考，实际税额可能因多种因素而异")
    print("=" * 70)


if __name__ == "__main__":
    main()
