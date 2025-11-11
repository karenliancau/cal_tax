#!/usr/bin/env python3
"""
美国联邦税计算器 - 命令行界面
US Federal Tax Calculator - CLI Interface
"""

import sys
from federal_tax import (
    FederalTaxCalculator,
    FilingStatus,
    format_currency,
    format_percentage
)


class FederalTaxCLI:
    """联邦税命令行界面"""

    def __init__(self):
        self.calculator = FederalTaxCalculator()
        self.running = True

    def display_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 70)
        print("美国联邦税计算器 | US Federal Tax Calculator")
        print("=" * 70)
        print("\n请选择计算类型:")
        print("1. 联邦所得税 (Federal Income Tax)")
        print("2. FICA税 (Social Security & Medicare)")
        print("3. 自雇税 (Self-Employment Tax)")
        print("4. 资本利得税 (Capital Gains Tax)")
        print("5. 标准扣除额 (Standard Deduction)")
        print("6. 综合税负计算 (Total Tax Liability)")
        print("7. 查看税级表 (View Tax Brackets)")
        print("0. 退出 (Exit)")
        print("-" * 70)

    def get_input(self, prompt: str, input_type=str, allow_empty=False):
        """获取并验证用户输入"""
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
        print("\n请选择报税身份 (Filing Status):")
        print("1. Single (单身)")
        print("2. Married Filing Jointly (已婚联合报税)")
        print("3. Married Filing Separately (已婚分别报税)")
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
                print("❌ 无效选择，请输入 1-4")

    def calculate_income_tax(self):
        """计算联邦所得税"""
        print("\n--- 联邦所得税计算 ---")

        filing_status = self.select_filing_status()

        taxable_income = self.get_input("请输入应税收入 ($): ", float)
        if taxable_income is None:
            return

        result = self.calculator.calculate_income_tax(taxable_income, filing_status)

        print("\n计算结果:")
        print(f"  应税收入: {format_currency(result['taxable_income'])}")
        print(f"  报税身份: {result['filing_status']}")
        print(f"  联邦所得税: {format_currency(result['total_tax'])}")
        print(f"  实际税率: {format_percentage(result['effective_rate'])}")

        print("\n税级明细:")
        for i, bracket in enumerate(result['bracket_details'], 1):
            print(f"  {i}. {bracket['bracket_range']}")
            print(f"     税率: {format_percentage(bracket['rate'] * 100)}")
            print(f"     应税额: {format_currency(bracket['taxable_amount'])}")
            print(f"     税额: {format_currency(bracket['tax_amount'])}")

    def calculate_fica(self):
        """计算FICA税"""
        print("\n--- FICA税计算 (社会保险税 & 医疗保险税) ---")

        filing_status = self.select_filing_status()

        wages = self.get_input("请输入工资收入 ($): ", float)
        if wages is None:
            return

        result = self.calculator.calculate_fica_tax(wages, filing_status)

        print("\n计算结果:")
        print(f"  工资: {format_currency(result['wages'])}")
        print(f"  社会保险税 (6.2%): {format_currency(result['social_security_tax'])}")
        print(f"  医疗保险税 (1.45%): {format_currency(result['medicare_tax'])}")

        if result['additional_medicare_tax'] > 0:
            print(f"  附加医疗保险税 (0.9%): {format_currency(result['additional_medicare_tax'])}")

        print(f"  FICA税总额: {format_currency(result['total_fica_tax'])}")
        print(f"\n  注: 社会保险税工资基数上限为 {format_currency(result['ss_wage_base'])}")

    def calculate_self_employment(self):
        """计算自雇税"""
        print("\n--- 自雇税计算 ---")

        net_earnings = self.get_input("请输入净收入 ($): ", float)
        if net_earnings is None:
            return

        result = self.calculator.calculate_self_employment_tax(net_earnings)

        print("\n计算结果:")
        print(f"  净收入: {format_currency(result['net_earnings'])}")
        print(f"  应税收入 (92.35%): {format_currency(result['taxable_earnings'])}")
        print(f"  社会保险税部分: {format_currency(result['social_security_tax'])}")
        print(f"  医疗保险税部分: {format_currency(result['medicare_tax'])}")
        print(f"  自雇税总额: {format_currency(result['total_se_tax'])}")
        print(f"  可扣除金额 (50%): {format_currency(result['deductible_amount'])}")

    def calculate_capital_gains(self):
        """计算资本利得税"""
        print("\n--- 资本利得税计算 ---")

        filing_status = self.select_filing_status()

        capital_gains = self.get_input("请输入资本利得 ($): ", float)
        if capital_gains is None:
            return

        ordinary_income = self.get_input("请输入普通收入 ($): ", float)
        if ordinary_income is None:
            return

        print("\n持有期限:")
        print("1. 长期 (> 1年)")
        print("2. 短期 (<= 1年)")
        period_choice = self.get_input("请选择 (1-2): ", str)
        holding_period = "long" if period_choice == "1" else "short"

        result = self.calculator.calculate_capital_gains_tax(
            capital_gains, ordinary_income, filing_status, holding_period
        )

        print("\n计算结果:")
        print(f"  资本利得: {format_currency(result['capital_gains'])}")
        print(f"  持有期限: {result['holding_period']}")

        if holding_period == "long":
            print(f"  适用税率: {format_percentage(result['primary_tax_rate'] * 100)}")
            print(f"  资本利得税: {format_currency(result['capital_gains_tax'])}")
            if result['net_investment_income_tax'] > 0:
                print(f"  净投资收入税 (3.8%): {format_currency(result['net_investment_income_tax'])}")
            print(f"  总税额: {format_currency(result['total_tax'])}")
        else:
            print(f"  税率: 按普通所得税率计税")
            print(f"  资本利得税: {format_currency(result['capital_gains_tax'])}")

    def calculate_standard_deduction(self):
        """计算标准扣除额"""
        print("\n--- 标准扣除额计算 ---")

        filing_status = self.select_filing_status()

        age_65_or_older = self.get_input("65岁或以上人数 (默认0): ", int, True) or 0
        blind = self.get_input("盲人人数 (默认0): ", int, True) or 0

        result = self.calculator.calculate_standard_deduction(
            filing_status, age_65_or_older, blind
        )

        print("\n计算结果:")
        print(f"  报税身份: {result['filing_status']}")
        print(f"  基础扣除额: {format_currency(result['base_deduction'])}")
        if result['additional_deduction'] > 0:
            print(f"  额外扣除额: {format_currency(result['additional_deduction'])}")
        print(f"  标准扣除额总计: {format_currency(result['total_standard_deduction'])}")

    def calculate_total_liability(self):
        """计算综合税负"""
        print("\n--- 综合税负计算 ---")

        filing_status = self.select_filing_status()

        gross_income = self.get_input("请输入总收入 ($): ", float)
        if gross_income is None:
            return

        self_employed = self.get_input("是否自雇? (y/n): ", str).lower() == 'y'

        print("\n是否有分项扣除? (y/n)")
        has_itemized = self.get_input("选择: ", str).lower() == 'y'
        itemized_deductions = 0
        if has_itemized:
            itemized_deductions = self.get_input("请输入分项扣除总额 ($): ", float) or 0

        capital_gains = self.get_input("资本利得 (默认0): ", float, True) or 0
        tax_credits = self.get_input("税收抵免 (默认0): ", float, True) or 0

        result = self.calculator.calculate_total_tax_liability(
            gross_income,
            filing_status,
            itemized_deductions,
            tax_credits,
            capital_gains,
            self_employed
        )

        print("\n" + "=" * 70)
        print("综合税务计算结果")
        print("=" * 70)

        print(f"\n收入信息:")
        print(f"  总收入: {format_currency(result['gross_income'])}")

        if result['agi_adjustments']:
            print(f"\n调整项:")
            for adj in result['agi_adjustments']:
                print(f"  - {adj['description']}: {format_currency(adj['amount'])}")

        print(f"  调整后总收入 (AGI): {format_currency(result['adjusted_gross_income'])}")

        print(f"\n扣除:")
        print(f"  扣除类型: {result['deduction_type']}")
        print(f"  扣除金额: {format_currency(result['deduction_amount'])}")
        print(f"  应税收入: {format_currency(result['taxable_income'])}")

        print(f"\n税额:")
        if result['income_tax'] > 0:
            print(f"  联邦所得税: {format_currency(result['income_tax'])}")
        if result['capital_gains_tax'] > 0:
            print(f"  资本利得税: {format_currency(result['capital_gains_tax'])}")
        if result['self_employment_tax'] > 0:
            print(f"  自雇税: {format_currency(result['self_employment_tax'])}")

        print(f"  税前总额: {format_currency(result['total_tax_before_credits'])}")

        if result['tax_credits'] > 0:
            print(f"  税收抵免: -{format_currency(result['tax_credits'])}")

        print(f"\n最终税负: {format_currency(result['total_tax_liability'])}")
        print(f"实际税率: {format_percentage(result['effective_tax_rate'])}")
        print("=" * 70)

    def view_tax_brackets(self):
        """查看税级表"""
        print("\n--- 2024年联邦所得税税级表 ---")

        filing_status = self.select_filing_status()

        brackets = self.calculator.TAX_BRACKETS_2024[filing_status]

        print(f"\n报税身份: {filing_status.value}")
        print("-" * 70)

        previous = 0
        for i, (limit, rate) in enumerate(brackets, 1):
            if limit == float('inf'):
                print(f"{i}. ${previous:,}+ : {format_percentage(rate * 100)}")
            else:
                print(f"{i}. ${previous:,} - ${limit:,} : {format_percentage(rate * 100)}")
                previous = int(limit)

        # 显示标准扣除额
        std_ded = self.calculator.STANDARD_DEDUCTION_2024[filing_status]
        print(f"\n标准扣除额: {format_currency(std_ded)}")

    def run(self):
        """运行主程序"""
        print("\n欢迎使用美国联邦税计算器!")
        print("Welcome to US Federal Tax Calculator!")
        print("Tax Year: 2024")

        while self.running:
            try:
                self.display_menu()
                choice = self.get_input("请选择 (0-7): ", str)

                if choice == "1":
                    self.calculate_income_tax()
                elif choice == "2":
                    self.calculate_fica()
                elif choice == "3":
                    self.calculate_self_employment()
                elif choice == "4":
                    self.calculate_capital_gains()
                elif choice == "5":
                    self.calculate_standard_deduction()
                elif choice == "6":
                    self.calculate_total_liability()
                elif choice == "7":
                    self.view_tax_brackets()
                elif choice == "0":
                    print("\n感谢使用！再见！")
                    self.running = False
                else:
                    print("❌ 无效选择，请输入 0-7 之间的数字")

            except KeyboardInterrupt:
                print("\n\n感谢使用！再见！")
                self.running = False
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                print("请重试或选择其他选项")


def main():
    """主函数"""
    cli = FederalTaxCLI()
    cli.run()


if __name__ == "__main__":
    main()
