#!/usr/bin/env python3
"""
田纳西州报税计算器 - 命令行界面
Tennessee Tax Calculator - CLI Interface
"""

import sys
from tennessee_tax import (
    TennesseeTaxCalculator,
    format_currency,
    format_percentage
)


class TaxCalculatorCLI:
    """命令行界面类"""

    def __init__(self):
        self.calculator = TennesseeTaxCalculator()
        self.running = True

    def display_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 60)
        print("田纳西州报税计算器 | Tennessee Tax Calculator")
        print("=" * 60)
        print("\n请选择要计算的税种:")
        print("1. 销售税 (Sales Tax)")
        print("2. 房产税 (Property Tax)")
        print("3. 商业税 (Business Tax)")
        print("4. 特许经营税 (Franchise Tax)")
        print("5. 查看支持的县列表 (View Counties)")
        print("6. 查看企业类型列表 (View Business Types)")
        print("0. 退出 (Exit)")
        print("-" * 60)

    def get_input(self, prompt: str, input_type=str, allow_empty=False):
        """获取用户输入并验证"""
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

    def calculate_sales_tax(self):
        """销售税计算流程"""
        print("\n--- 销售税计算 ---")

        amount = self.get_input("请输入商品/服务金额 ($): ", float)
        if amount is None:
            return

        county = self.get_input(
            "请输入县名 (如 Davidson, Shelby，按回车使用默认): ",
            str,
            allow_empty=True
        ) or "default"

        result = self.calculator.calculate_sales_tax(amount, county)

        print("\n计算结果:")
        print(f"  商品金额: {format_currency(result['amount'])}")
        print(f"  县: {result['county']}")
        print(f"  税率: {format_percentage(result['tax_rate'])}")
        print(f"  销售税: {format_currency(result['tax_amount'])}")
        print(f"  总计: {format_currency(result['total'])}")

    def calculate_property_tax(self):
        """房产税计算流程"""
        print("\n--- 房产税计算 ---")

        market_value = self.get_input("请输入房产市场价值 ($): ", float)
        if market_value is None:
            return

        county = self.get_input(
            "请输入县名 (如 Davidson, Shelby，按回车使用默认): ",
            str,
            allow_empty=True
        ) or "default"

        result = self.calculator.calculate_property_tax(market_value, county)

        print("\n计算结果:")
        print(f"  市场价值: {format_currency(result['market_value'])}")
        print(f"  评估价值 (25%): {format_currency(result['assessed_value'])}")
        print(f"  县: {result['county']}")
        print(f"  税率: ${result['tax_rate_per_100']:.2f} 每 $100 评估价值")
        print(f"  年度房产税: {format_currency(result['annual_tax'])}")
        print(f"  月均房产税: {format_currency(result['annual_tax'] / 12)}")

    def calculate_business_tax(self):
        """商业税计算流程"""
        print("\n--- 商业税计算 ---")

        gross_receipts = self.get_input("请输入企业总收入 ($): ", float)
        if gross_receipts is None:
            return

        print("\n可用的企业类型:")
        types = self.calculator.get_available_business_types()
        for i, btype in enumerate(types, 1):
            print(f"  {i}. {btype}")

        business_type = self.get_input(
            "请输入企业类型 (按回车使用默认): ",
            str,
            allow_empty=True
        ) or "default"

        result = self.calculator.calculate_business_tax(gross_receipts, business_type)

        print("\n计算结果:")
        print(f"  总收入: {format_currency(result['gross_receipts'])}")
        print(f"  企业类型: {result['business_type']}")
        print(f"  税率: {format_percentage(result['tax_rate'])}")
        print(f"  商业税: {format_currency(result['tax_amount'])}")

    def calculate_franchise_tax(self):
        """特许经营税计算流程"""
        print("\n--- 特许经营税计算 ---")

        net_worth = self.get_input("请输入企业净资产 ($): ", float)
        if net_worth is None:
            return

        result = self.calculator.calculate_franchise_tax(net_worth)

        print("\n计算结果:")
        print(f"  净资产: {format_currency(result['net_worth'])}")
        print(f"  税率: {format_percentage(result['tax_rate'])}")
        print(f"  最低税额: {format_currency(result['minimum_tax'])}")
        print(f"  应缴税额: {format_currency(result['tax_amount'])}")

    def show_counties(self):
        """显示支持的县列表"""
        print("\n--- 支持的县 ---")
        counties = self.calculator.get_available_counties()
        for i, county in enumerate(counties, 1):
            sales_rate = self.calculator.SALES_TAX_RATES.get(county, 0)
            prop_rate = self.calculator.PROPERTY_TAX_RATES.get(county, 0)
            print(f"{i:2d}. {county:15s} - 销售税: {format_percentage(sales_rate)}, "
                  f"房产税: ${prop_rate:.2f}/$100")

    def show_business_types(self):
        """显示企业类型列表"""
        print("\n--- 企业类型及税率 ---")
        types = self.calculator.get_available_business_types()
        for i, btype in enumerate(types, 1):
            rate = self.calculator.BUSINESS_TAX_RATES.get(btype, 0)
            print(f"{i}. {btype:15s} - {format_percentage(rate)}")

    def run(self):
        """运行主程序"""
        print("\n欢迎使用田纳西州报税计算器!")
        print("Welcome to Tennessee Tax Calculator!")

        while self.running:
            try:
                self.display_menu()
                choice = self.get_input("请选择 (0-6): ", str)

                if choice == "1":
                    self.calculate_sales_tax()
                elif choice == "2":
                    self.calculate_property_tax()
                elif choice == "3":
                    self.calculate_business_tax()
                elif choice == "4":
                    self.calculate_franchise_tax()
                elif choice == "5":
                    self.show_counties()
                elif choice == "6":
                    self.show_business_types()
                elif choice == "0":
                    print("\n感谢使用！再见！")
                    self.running = False
                else:
                    print("❌ 无效选择，请输入 0-6 之间的数字")

            except KeyboardInterrupt:
                print("\n\n感谢使用！再见！")
                self.running = False
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                print("请重试或选择其他选项")


def main():
    """主函数"""
    cli = TaxCalculatorCLI()
    cli.run()


if __name__ == "__main__":
    main()
