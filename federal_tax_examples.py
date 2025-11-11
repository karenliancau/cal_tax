"""
美国联邦税计算器使用示例
US Federal Tax Calculator Usage Examples
"""

from federal_tax import (
    FederalTaxCalculator,
    FilingStatus,
    format_currency,
    format_percentage
)


def print_section_header(title):
    """打印章节标题"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def example_1_income_tax():
    """示例1: 基本所得税计算"""
    print_section_header("示例 1: 联邦所得税计算")

    calculator = FederalTaxCalculator()

    # 单身纳税人，应税收入$75,000
    result = calculator.calculate_income_tax(75000, FilingStatus.SINGLE)

    print(f"\n报税身份: Single (单身)")
    print(f"应税收入: {format_currency(result['taxable_income'])}")
    print(f"联邦所得税: {format_currency(result['total_tax'])}")
    print(f"实际税率: {format_percentage(result['effective_rate'])}")

    print(f"\n税级明细:")
    for i, bracket in enumerate(result['bracket_details'], 1):
        print(f"  {i}. {bracket['bracket_range']}")
        print(f"     税率: {format_percentage(bracket['rate'] * 100)}")
        print(f"     此税级应税额: {format_currency(bracket['taxable_amount'])}")
        print(f"     此税级税额: {format_currency(bracket['tax_amount'])}")


def example_2_fica_tax():
    """示例2: FICA税计算"""
    print_section_header("示例 2: FICA税计算 (社会保险税 & 医疗保险税)")

    calculator = FederalTaxCalculator()

    # 工资收入$85,000
    result = calculator.calculate_fica_tax(85000, FilingStatus.SINGLE)

    print(f"\n年度工资: {format_currency(result['wages'])}")
    print(f"\n社会保险税 (6.2%): {format_currency(result['social_security_tax'])}")
    print(f"  工资基数上限: {format_currency(result['ss_wage_base'])}")
    print(f"\n医疗保险税 (1.45%): {format_currency(result['medicare_tax'])}")

    if result['additional_medicare_tax'] > 0:
        print(f"附加医疗保险税 (0.9%): {format_currency(result['additional_medicare_tax'])}")

    print(f"\nFICA税总额: {format_currency(result['total_fica_tax'])}")
    print(f"净工资 (扣除FICA后): {format_currency(result['wages'] - result['total_fica_tax'])}")


def example_3_self_employment():
    """示例3: 自雇税计算"""
    print_section_header("示例 3: 自雇税计算")

    calculator = FederalTaxCalculator()

    # 自由职业者净收入$80,000
    result = calculator.calculate_self_employment_tax(80000)

    print(f"\n净收入: {format_currency(result['net_earnings'])}")
    print(f"应税收入 (92.35%): {format_currency(result['taxable_earnings'])}")
    print(f"\n社会保险税部分 (12.4%): {format_currency(result['social_security_tax'])}")
    print(f"医疗保险税部分 (2.9%): {format_currency(result['medicare_tax'])}")
    print(f"\n自雇税总额: {format_currency(result['total_se_tax'])}")
    print(f"可在报税时扣除 (50%): {format_currency(result['deductible_amount'])}")
    print(f"\n注: 自雇人士需支付雇主和雇员双方的社保和医保税")


def example_4_capital_gains():
    """示例4: 资本利得税计算"""
    print_section_header("示例 4: 资本利得税计算")

    calculator = FederalTaxCalculator()

    # 场景A: 长期资本利得
    print("\n场景A: 长期资本利得 (持有超过1年)")
    print("-" * 80)

    long_term_result = calculator.calculate_capital_gains_tax(
        capital_gains=30000,
        ordinary_income=70000,
        filing_status=FilingStatus.SINGLE,
        holding_period="long"
    )

    print(f"普通收入: {format_currency(70000)}")
    print(f"长期资本利得: {format_currency(long_term_result['capital_gains'])}")
    print(f"适用税率: {format_percentage(long_term_result['primary_tax_rate'] * 100)}")
    print(f"资本利得税: {format_currency(long_term_result['capital_gains_tax'])}")

    if long_term_result['net_investment_income_tax'] > 0:
        print(f"净投资收入税 (3.8%): {format_currency(long_term_result['net_investment_income_tax'])}")

    print(f"总税额: {format_currency(long_term_result['total_tax'])}")

    # 场景B: 短期资本利得
    print("\n场景B: 短期资本利得 (持有不超过1年)")
    print("-" * 80)

    short_term_result = calculator.calculate_capital_gains_tax(
        capital_gains=30000,
        ordinary_income=70000,
        filing_status=FilingStatus.SINGLE,
        holding_period="short"
    )

    print(f"短期资本利得: {format_currency(short_term_result['capital_gains'])}")
    print(f"税率: 按普通所得税率计税")
    print(f"资本利得税: {format_currency(short_term_result['capital_gains_tax'])}")
    print(f"\n提示: 长期资本利得税率更优惠!")


def example_5_standard_deduction():
    """示例5: 标准扣除额"""
    print_section_header("示例 5: 标准扣除额计算")

    calculator = FederalTaxCalculator()

    print("\n不同报税身份的标准扣除额 (2024年):\n")

    filing_statuses = [
        (FilingStatus.SINGLE, "Single (单身)"),
        (FilingStatus.MARRIED_JOINTLY, "Married Filing Jointly (已婚联合)"),
        (FilingStatus.MARRIED_SEPARATELY, "Married Filing Separately (已婚分别)"),
        (FilingStatus.HEAD_OF_HOUSEHOLD, "Head of Household (户主)")
    ]

    for status, name in filing_statuses:
        result = calculator.calculate_standard_deduction(status)
        print(f"{name:40s}: {format_currency(result['total_standard_deduction'])}")

    # 65岁以上或盲人的额外扣除
    print("\n特殊情况 - 单身纳税人:")
    print("-" * 80)

    # 65岁以上
    senior_result = calculator.calculate_standard_deduction(
        FilingStatus.SINGLE,
        age_65_or_older=1
    )
    print(f"65岁或以上: 基础 {format_currency(senior_result['base_deduction'])} "
          f"+ 额外 {format_currency(senior_result['additional_deduction'])} "
          f"= {format_currency(senior_result['total_standard_deduction'])}")

    # 盲人
    blind_result = calculator.calculate_standard_deduction(
        FilingStatus.SINGLE,
        blind=1
    )
    print(f"盲人:       基础 {format_currency(blind_result['base_deduction'])} "
          f"+ 额外 {format_currency(blind_result['additional_deduction'])} "
          f"= {format_currency(blind_result['total_standard_deduction'])}")


def example_6_comprehensive_calculation():
    """示例6: 综合税务计算"""
    print_section_header("示例 6: 综合税务计算 - W-2雇员")

    calculator = FederalTaxCalculator()

    # 场景: W-2雇员，年薪$90,000
    result = calculator.calculate_total_tax_liability(
        gross_income=90000,
        filing_status=FilingStatus.SINGLE,
        itemized_deductions=0,  # 使用标准扣除
        tax_credits=0,
        capital_gains=0,
        self_employed=False
    )

    print(f"\n收入:")
    print(f"  总收入 (W-2工资): {format_currency(result['gross_income'])}")
    print(f"  调整后总收入 (AGI): {format_currency(result['adjusted_gross_income'])}")

    print(f"\n扣除:")
    print(f"  扣除类型: {result['deduction_type']}")
    print(f"  扣除金额: {format_currency(result['deduction_amount'])}")

    print(f"\n应税收入:")
    print(f"  {format_currency(result['taxable_income'])}")

    print(f"\n税额:")
    print(f"  联邦所得税: {format_currency(result['income_tax'])}")

    # 计算FICA (雇员部分)
    fica_result = calculator.calculate_fica_tax(90000, FilingStatus.SINGLE)
    print(f"  FICA税 (雇员部分): {format_currency(fica_result['total_fica_tax'])}")

    total_federal = result['total_tax_liability'] + fica_result['total_fica_tax']

    print(f"\n总联邦税负:")
    print(f"  所得税 + FICA税: {format_currency(total_federal)}")
    print(f"  实际税率: {format_percentage(total_federal / 90000 * 100)}")
    print(f"\n税后收入: {format_currency(90000 - total_federal)}")


def example_7_self_employed_comprehensive():
    """示例7: 自雇人士综合计算"""
    print_section_header("示例 7: 自雇人士综合税务计算")

    calculator = FederalTaxCalculator()

    # 场景: 自由职业者，年净收入$120,000
    result = calculator.calculate_total_tax_liability(
        gross_income=120000,
        filing_status=FilingStatus.SINGLE,
        itemized_deductions=0,
        tax_credits=2500,  # 假设有一些税收抵免
        capital_gains=0,
        self_employed=True
    )

    print(f"\n收入:")
    print(f"  净收入 (Schedule C): {format_currency(result['gross_income'])}")

    if result['agi_adjustments']:
        print(f"\nAGI调整:")
        for adj in result['agi_adjustments']:
            print(f"  {adj['description']}: -{format_currency(adj['amount'])}")

    print(f"  调整后总收入 (AGI): {format_currency(result['adjusted_gross_income'])}")

    print(f"\n扣除:")
    print(f"  {result['deduction_type']}扣除: {format_currency(result['deduction_amount'])}")
    print(f"  应税收入: {format_currency(result['taxable_income'])}")

    print(f"\n税额:")
    print(f"  联邦所得税: {format_currency(result['income_tax'])}")
    print(f"  自雇税: {format_currency(result['self_employment_tax'])}")
    print(f"  税前总额: {format_currency(result['total_tax_before_credits'])}")

    if result['tax_credits'] > 0:
        print(f"\n税收抵免:")
        print(f"  -{format_currency(result['tax_credits'])}")

    print(f"\n最终税负: {format_currency(result['total_tax_liability'])}")
    print(f"实际税率: {format_percentage(result['effective_tax_rate'])}")

    net_income = result['gross_income'] - result['total_tax_liability']
    print(f"\n税后净收入: {format_currency(net_income)}")


def example_8_married_couple():
    """示例8: 已婚夫妇"""
    print_section_header("示例 8: 已婚夫妇联合报税")

    calculator = FederalTaxCalculator()

    # 场景: 已婚夫妇，总收入$150,000，有资本利得$25,000
    result = calculator.calculate_total_tax_liability(
        gross_income=150000,
        filing_status=FilingStatus.MARRIED_JOINTLY,
        itemized_deductions=32000,  # 房贷利息、州税等
        tax_credits=4000,  # 子女税收抵免等
        capital_gains=25000,
        self_employed=False
    )

    print(f"\n家庭收入:")
    print(f"  W-2工资总计: {format_currency(result['gross_income'])}")
    print(f"  资本利得: {format_currency(25000)}")
    print(f"  调整后总收入: {format_currency(result['adjusted_gross_income'])}")

    print(f"\n扣除:")
    print(f"  {result['deduction_type']}扣除: {format_currency(result['deduction_amount'])}")
    print(f"  应税收入: {format_currency(result['taxable_income'])}")

    print(f"\n税额:")
    print(f"  联邦所得税: {format_currency(result['income_tax'])}")
    print(f"  资本利得税: {format_currency(result['capital_gains_tax'])}")
    print(f"  税前总额: {format_currency(result['total_tax_before_credits'])}")
    print(f"  税收抵免: -{format_currency(result['tax_credits'])}")

    print(f"\n最终税负: {format_currency(result['total_tax_liability'])}")
    print(f"实际税率: {format_percentage(result['effective_tax_rate'])}")

    # 计算双方的FICA
    fica_result = calculator.calculate_fica_tax(150000, FilingStatus.MARRIED_JOINTLY)
    total_federal = result['total_tax_liability'] + fica_result['total_fica_tax']

    print(f"\n加上FICA税: {format_currency(fica_result['total_fica_tax'])}")
    print(f"总联邦税负: {format_currency(total_federal)}")


def example_9_comparison():
    """示例9: 不同报税身份比较"""
    print_section_header("示例 9: 不同报税身份税负比较")

    calculator = FederalTaxCalculator()
    income = 80000

    print(f"\n相同收入 ({format_currency(income)}) 在不同报税身份下的税负:\n")

    statuses = [
        (FilingStatus.SINGLE, "Single"),
        (FilingStatus.MARRIED_JOINTLY, "Married Jointly"),
        (FilingStatus.MARRIED_SEPARATELY, "Married Separately"),
        (FilingStatus.HEAD_OF_HOUSEHOLD, "Head of Household")
    ]

    results = []
    for status, name in statuses:
        # 计算应税收入（减去标准扣除）
        std_ded = calculator.calculate_standard_deduction(status)
        taxable = income - std_ded['total_standard_deduction']

        tax_result = calculator.calculate_income_tax(taxable, status)

        results.append({
            'name': name,
            'deduction': std_ded['total_standard_deduction'],
            'taxable': taxable,
            'tax': tax_result['total_tax'],
            'rate': tax_result['effective_rate']
        })

    print(f"{'报税身份':<25} {'标准扣除':<15} {'应税收入':<15} {'所得税':<15} {'税率'}")
    print("-" * 80)

    for r in results:
        print(f"{r['name']:<25} "
              f"{format_currency(r['deduction']):<15} "
              f"{format_currency(r['taxable']):<15} "
              f"{format_currency(r['tax']):<15} "
              f"{format_percentage(r['rate'])}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 80)
    print("美国联邦税计算器 - 详细示例")
    print("US Federal Tax Calculator - Comprehensive Examples")
    print("Tax Year: 2024")
    print("=" * 80)

    example_1_income_tax()
    example_2_fica_tax()
    example_3_self_employment()
    example_4_capital_gains()
    example_5_standard_deduction()
    example_6_comprehensive_calculation()
    example_7_self_employed_comprehensive()
    example_8_married_couple()
    example_9_comparison()

    print("\n" + "=" * 80)
    print("⚠️  免责声明:")
    print("以上计算结果仅供参考和教育目的。实际税务情况可能更复杂，")
    print("建议咨询专业税务顾问或使用IRS官方工具。")
    print("税率和法规可能会变化，请以当年IRS公布的数据为准。")
    print("=" * 80)


if __name__ == "__main__":
    main()
