#!/usr/bin/env python3
"""
综合税务计算器 - 美国联邦税 + 田纳西州税
Comprehensive Tax Calculator - US Federal + Tennessee State Taxes
"""

import sys
from federal_tax import FederalTaxCalculator, FilingStatus, format_currency, format_percentage
from tennessee_tax import TennesseeTaxCalculator


class ComprehensiveTaxCLI:
    """综合税务计算器CLI"""

    def __init__(self):
        self.federal_calc = FederalTaxCalculator()
        self.tn_calc = TennesseeTaxCalculator()
        self.running = True

    def display_main_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 80)
        print("美国税务计算器 | US Tax Calculator")
        print("Federal Taxes + Tennessee State Taxes")
        print("=" * 80)
        print("\n请选择税务类型:")
        print("1. 联邦税计算 (Federal Taxes)")
        print("2. 田纳西州税计算 (Tennessee State Taxes)")
        print("3. 综合计算 - 联邦+州税 (Comprehensive Calculation)")
        print("4. 税务规划工具 (Tax Planning Tools)")
        print("0. 退出 (Exit)")
        print("-" * 80)

    def display_federal_menu(self):
        """显示联邦税菜单"""
        print("\n--- 联邦税计算 ---")
        print("1. 联邦所得税 (Income Tax)")
        print("2. FICA税 (Social Security & Medicare)")
        print("3. 自雇税 (Self-Employment Tax)")
        print("4. 资本利得税 (Capital Gains Tax)")
        print("5. 标准扣除额 (Standard Deduction)")
        print("6. 综合联邦税负 (Total Federal Liability)")
        print("0. 返回主菜单")

    def display_tennessee_menu(self):
        """显示田纳西州税菜单"""
        print("\n--- 田纳西州税计算 ---")
        print("1. 销售税 (Sales Tax)")
        print("2. 房产税 (Property Tax)")
        print("3. 商业税 (Business Tax)")
        print("4. 特许经营税 (Franchise Tax)")
        print("0. 返回主菜单")

    def get_input(self, prompt: str, input_type=str, allow_empty=False):
        """获取用户输入"""
        while True:
            try:
                value = input(prompt).strip()
                if not value and allow_empty:
                    return None
                if input_type == float:
                    return float(value)
                elif input_type == int:
                    return int(value)
                else:
                    return value
            except ValueError:
                print(f"❌ 输入无效，请输入{input_type.__name__}类型的值")
            except KeyboardInterrupt:
                print("\n\n已取消操作")
                return None

    def select_filing_status(self) -> FilingStatus:
        """选择报税身份"""
        print("\n报税身份 (Filing Status):")
        print("1. Single (单身)")
        print("2. Married Filing Jointly (已婚联合)")
        print("3. Married Filing Separately (已婚分别)")
        print("4. Head of Household (户主)")

        while True:
            choice = self.get_input("请选择 (1-4): ", str)
            if choice == "1":
                return FilingStatus.SINGLE
            elif choice == "2":
                return FilingStatus.MARRIED_JOINTLY
            elif choice == "3":
                return FilingStatus.MARRIED_SEPARATELY
            elif choice == "4":
                return FilingStatus.HEAD_OF_HOUSEHOLD
            else:
                print("❌ 无效选择")

    def comprehensive_calculation(self):
        """综合计算 - 联邦税 + 田纳西州税"""
        print("\n" + "=" * 80)
        print("综合税务计算 - 田纳西州居民完整税负")
        print("=" * 80)

        # 收集基本信息
        filing_status = self.select_filing_status()

        gross_income = self.get_input("\n请输入年度总收入 ($): ", float)
        if gross_income is None:
            return

        self_employed = self.get_input("是否自雇? (y/n): ", str).lower() == 'y'

        # 分项扣除
        print("\n是否有分项扣除? (如房贷利息、慈善捐款等)")
        has_itemized = self.get_input("(y/n): ", str).lower() == 'y'
        itemized_deductions = 0
        if has_itemized:
            itemized_deductions = self.get_input("分项扣除总额 ($): ", float) or 0

        # 资本利得
        capital_gains = self.get_input("长期资本利得 (默认0): ", float, True) or 0

        # 税收抵免
        tax_credits = self.get_input("联邦税收抵免 (默认0): ", float, True) or 0

        # 田纳西州相关
        print("\n--- 田纳西州税务信息 ---")

        # 房产
        has_property = self.get_input("是否拥有房产? (y/n): ", str).lower() == 'y'
        property_value = 0
        county = "default"
        if has_property:
            property_value = self.get_input("房产市场价值 ($): ", float) or 0
            county = self.get_input("所在县 (如Davidson, Shelby，默认): ", str, True) or "default"

        # 计算联邦税
        print("\n正在计算联邦税...")
        federal_result = self.federal_calc.calculate_total_tax_liability(
            gross_income=gross_income,
            filing_status=filing_status,
            itemized_deductions=itemized_deductions,
            tax_credits=tax_credits,
            capital_gains=capital_gains,
            self_employed=self_employed
        )

        # 计算FICA (如果不是自雇)
        fica_tax = 0
        if not self_employed:
            fica_result = self.federal_calc.calculate_fica_tax(gross_income, filing_status)
            fica_tax = fica_result['total_fica_tax']

        # 计算田纳西州房产税
        tn_property_tax = 0
        if has_property and property_value > 0:
            prop_result = self.tn_calc.calculate_property_tax(property_value, county)
            tn_property_tax = prop_result['annual_tax']

        # 显示结果
        print("\n" + "=" * 80)
        print("完整税务计算结果")
        print("=" * 80)

        print(f"\n【收入】")
        print(f"  总收入: {format_currency(gross_income)}")
        print(f"  调整后总收入 (AGI): {format_currency(federal_result['adjusted_gross_income'])}")

        print(f"\n【联邦税】")
        print(f"  应税收入: {format_currency(federal_result['taxable_income'])}")
        print(f"  联邦所得税: {format_currency(federal_result['income_tax'])}")

        if federal_result['capital_gains_tax'] > 0:
            print(f"  资本利得税: {format_currency(federal_result['capital_gains_tax'])}")

        if federal_result['self_employment_tax'] > 0:
            print(f"  自雇税: {format_currency(federal_result['self_employment_tax'])}")
        elif fica_tax > 0:
            print(f"  FICA税 (雇员部分): {format_currency(fica_tax)}")

        if federal_result['tax_credits'] > 0:
            print(f"  税收抵免: -{format_currency(federal_result['tax_credits'])}")

        total_federal = federal_result['total_tax_liability']
        if not self_employed:
            total_federal += fica_tax

        print(f"  联邦税总计: {format_currency(total_federal)}")

        print(f"\n【田纳西州税】")
        print(f"  州所得税: $0.00 (田纳西州无个人所得税)")

        if tn_property_tax > 0:
            print(f"  房产税 ({county} County): {format_currency(tn_property_tax)}")
            print(f"    - 月均: {format_currency(tn_property_tax / 12)}")

        print(f"  州税总计: {format_currency(tn_property_tax)}")

        # 总计
        total_tax = total_federal + tn_property_tax

        print(f"\n【总税负】")
        print(f"  联邦税: {format_currency(total_federal)}")
        print(f"  州税: {format_currency(tn_property_tax)}")
        print(f"  总税额: {format_currency(total_tax)}")
        print(f"  总实际税率: {format_percentage(total_tax / gross_income * 100)}")

        print(f"\n【税后收入】")
        net_income = gross_income - total_tax
        print(f"  年度税后收入: {format_currency(net_income)}")
        print(f"  月均税后收入: {format_currency(net_income / 12)}")

        if has_property and tn_property_tax > 0:
            monthly_mortgage_tax = tn_property_tax / 12
            print(f"\n【住房相关】")
            print(f"  月均房产税: {format_currency(monthly_mortgage_tax)}")
            print(f"  (通常包含在月供中)")

        print("=" * 80)

    def tax_planning_tools(self):
        """税务规划工具"""
        print("\n--- 税务规划工具 ---")
        print("1. 比较不同报税身份")
        print("2. 标准扣除 vs 分项扣除比较")
        print("3. 退休账户供款节税计算")
        print("4. 边际税率 vs 实际税率说明")
        print("0. 返回主菜单")

        choice = self.get_input("\n请选择: ", str)

        if choice == "1":
            self.compare_filing_statuses()
        elif choice == "2":
            self.compare_deductions()
        elif choice == "3":
            self.retirement_contribution_savings()
        elif choice == "4":
            self.explain_tax_rates()

    def compare_filing_statuses(self):
        """比较不同报税身份"""
        print("\n--- 比较不同报税身份的税负 ---")

        income = self.get_input("请输入收入 ($): ", float)
        if income is None:
            return

        print(f"\n收入 {format_currency(income)} 在不同报税身份下的税负:\n")

        statuses = [
            (FilingStatus.SINGLE, "Single"),
            (FilingStatus.MARRIED_JOINTLY, "Married Jointly"),
            (FilingStatus.HEAD_OF_HOUSEHOLD, "Head of Household")
        ]

        print(f"{'报税身份':<20} {'标准扣除':<15} {'所得税':<15} {'实际税率'}")
        print("-" * 65)

        for status, name in statuses:
            std_ded = self.federal_calc.calculate_standard_deduction(status)
            taxable = max(income - std_ded['total_standard_deduction'], 0)
            tax_result = self.federal_calc.calculate_income_tax(taxable, status)

            print(f"{name:<20} "
                  f"{format_currency(std_ded['total_standard_deduction']):<15} "
                  f"{format_currency(tax_result['total_tax']):<15} "
                  f"{format_percentage(tax_result['effective_rate'])}")

    def compare_deductions(self):
        """比较标准扣除和分项扣除"""
        print("\n--- 标准扣除 vs 分项扣除比较 ---")

        filing_status = self.select_filing_status()

        std_result = self.federal_calc.calculate_standard_deduction(filing_status)
        standard_amount = std_result['total_standard_deduction']

        print(f"\n您的标准扣除额: {format_currency(standard_amount)}")

        print("\n请输入您的分项扣除项目 (输入0跳过):")
        mortgage_interest = self.get_input("  房贷利息: $", float, True) or 0
        property_taxes = self.get_input("  房产税: $", float, True) or 0
        state_taxes = self.get_input("  州税和地方税 (SALT, 上限$10,000): $", float, True) or 0
        state_taxes = min(state_taxes, 10000)  # SALT上限
        charitable = self.get_input("  慈善捐款: $", float, True) or 0

        total_itemized = mortgage_interest + property_taxes + state_taxes + charitable

        print(f"\n分项扣除总额: {format_currency(total_itemized)}")
        print(f"标准扣除额: {format_currency(standard_amount)}")

        if total_itemized > standard_amount:
            savings = total_itemized - standard_amount
            print(f"\n✓ 建议使用分项扣除")
            print(f"  额外扣除: {format_currency(savings)}")
            print(f"  潜在节税 (按22%税率): ~{format_currency(savings * 0.22)}")
        else:
            print(f"\n✓ 建议使用标准扣除")
            print(f"  更简单，且金额更大")

    def retirement_contribution_savings(self):
        """退休账户供款节税"""
        print("\n--- 退休账户供款节税计算 ---")

        filing_status = self.select_filing_status()

        income = self.get_input("当前年收入 ($): ", float)
        if income is None:
            return

        contribution = self.get_input("计划供款至401(k)/Traditional IRA ($): ", float)
        if contribution is None:
            return

        # 2024年401(k)限额: $23,000 (50岁以下)
        max_401k = 23000
        if contribution > max_401k:
            print(f"⚠️  注意: 2024年401(k)供款限额为 {format_currency(max_401k)} (50岁以下)")

        # 计算供款前的税负
        std_ded = self.federal_calc.calculate_standard_deduction(filing_status)
        taxable_before = max(income - std_ded['total_standard_deduction'], 0)
        tax_before = self.federal_calc.calculate_income_tax(taxable_before, filing_status)

        # 计算供款后的税负
        reduced_income = income - contribution
        taxable_after = max(reduced_income - std_ded['total_standard_deduction'], 0)
        tax_after = self.federal_calc.calculate_income_tax(taxable_after, filing_status)

        # 节税金额
        tax_savings = tax_before['total_tax'] - tax_after['total_tax']

        print(f"\n供款前:")
        print(f"  收入: {format_currency(income)}")
        print(f"  联邦所得税: {format_currency(tax_before['total_tax'])}")

        print(f"\n供款后:")
        print(f"  应税收入: {format_currency(reduced_income)}")
        print(f"  联邦所得税: {format_currency(tax_after['total_tax'])}")

        print(f"\n节税效果:")
        print(f"  供款金额: {format_currency(contribution)}")
        print(f"  立即节税: {format_currency(tax_savings)}")
        print(f"  实际成本: {format_currency(contribution - tax_savings)}")
        print(f"  节税比例: {format_percentage(tax_savings / contribution * 100)}")

    def explain_tax_rates(self):
        """解释边际税率和实际税率"""
        print("\n--- 边际税率 vs 实际税率 ---")
        print("\n边际税率: 您下一美元收入将被征税的税率")
        print("实际税率: 您实际支付的税款占总收入的百分比")

        filing_status = self.select_filing_status()
        income = self.get_input("\n收入 ($): ", float)
        if income is None:
            return

        std_ded = self.federal_calc.calculate_standard_deduction(filing_status)
        taxable = max(income - std_ded['total_standard_deduction'], 0)
        result = self.federal_calc.calculate_income_tax(taxable, filing_status)

        # 找到边际税率
        brackets = self.federal_calc.TAX_BRACKETS_2024[filing_status]
        marginal_rate = 0
        for limit, rate in brackets:
            if taxable <= limit:
                marginal_rate = rate
                break

        print(f"\n收入: {format_currency(income)}")
        print(f"应税收入: {format_currency(taxable)}")
        print(f"\n边际税率: {format_percentage(marginal_rate * 100)}")
        print(f"  (您的下$1,000收入将被征收 {format_currency(1000 * marginal_rate)})")
        print(f"\n实际税率: {format_percentage(result['effective_rate'])}")
        print(f"  (您实际支付了 {format_currency(result['total_tax'])})")

        print(f"\n理解: 虽然您的边际税率是 {format_percentage(marginal_rate * 100)},")
        print(f"但由于累进税制，您的实际税率只有 {format_percentage(result['effective_rate'])}")

    def run(self):
        """运行主程序"""
        print("\n" + "=" * 80)
        print("欢迎使用综合税务计算器！")
        print("Welcome to Comprehensive Tax Calculator!")
        print("=" * 80)
        print("\n特色功能:")
        print("✓ 2024年联邦税计算（所得税、FICA、自雇税、资本利得税）")
        print("✓ 田纳西州税计算（销售税、房产税、商业税）")
        print("✓ 综合税负分析")
        print("✓ 税务规划工具")

        while self.running:
            try:
                self.display_main_menu()
                choice = self.get_input("请选择 (0-4): ", str)

                if choice == "1":
                    # 联邦税菜单
                    self.display_federal_menu()
                    fed_choice = self.get_input("请选择: ", str)
                    # 调用联邦税CLI的相应功能
                    # (这里可以导入并使用federal_tax_cli的功能)
                    print("请使用 'python federal_tax_cli.py' 查看详细联邦税功能")

                elif choice == "2":
                    # 田纳西州税菜单
                    self.display_tennessee_menu()
                    tn_choice = self.get_input("请选择: ", str)
                    # 调用田纳西州税CLI的相应功能
                    print("请使用 'python tn_tax_calculator.py' 查看详细州税功能")

                elif choice == "3":
                    self.comprehensive_calculation()

                elif choice == "4":
                    self.tax_planning_tools()

                elif choice == "0":
                    print("\n感谢使用！再见！")
                    self.running = False

                else:
                    print("❌ 无效选择")

            except KeyboardInterrupt:
                print("\n\n感谢使用！再见！")
                self.running = False
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")


def main():
    """主函数"""
    cli = ComprehensiveTaxCLI()
    cli.run()


if __name__ == "__main__":
    main()
