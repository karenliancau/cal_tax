"""
美国联邦税计算器测试
US Federal Tax Calculator Tests
"""

import unittest
from federal_tax import FederalTaxCalculator, FilingStatus


class TestFederalIncomeTax(unittest.TestCase):
    """测试联邦所得税计算"""

    def setUp(self):
        self.calculator = FederalTaxCalculator()

    def test_single_low_income(self):
        """测试单身低收入"""
        result = self.calculator.calculate_income_tax(50000, FilingStatus.SINGLE)
        # 应该在10%和12%税级
        self.assertEqual(result['taxable_income'], 50000)
        self.assertGreater(result['total_tax'], 0)
        self.assertLess(result['effective_rate'], 13)  # 实际税率约12.1%

    def test_single_high_income(self):
        """测试单身高收入"""
        result = self.calculator.calculate_income_tax(600000, FilingStatus.SINGLE)
        self.assertEqual(result['taxable_income'], 600000)
        # 高收入应该有较高的有效税率
        self.assertGreater(result['effective_rate'], 30)

    def test_married_jointly(self):
        """测试已婚联合报税"""
        result = self.calculator.calculate_income_tax(100000, FilingStatus.MARRIED_JOINTLY)
        self.assertEqual(result['taxable_income'], 100000)
        # 已婚联合的税负应该低于单身
        single_result = self.calculator.calculate_income_tax(100000, FilingStatus.SINGLE)
        self.assertLess(result['total_tax'], single_result['total_tax'])

    def test_head_of_household(self):
        """测试户主"""
        result = self.calculator.calculate_income_tax(80000, FilingStatus.HEAD_OF_HOUSEHOLD)
        self.assertEqual(result['taxable_income'], 80000)
        self.assertGreater(result['total_tax'], 0)

    def test_bracket_details(self):
        """测试税级明细"""
        result = self.calculator.calculate_income_tax(100000, FilingStatus.SINGLE)
        # 应该有多个税级
        self.assertGreater(len(result['bracket_details']), 1)
        # 验证税级明细结构
        for bracket in result['bracket_details']:
            self.assertIn('bracket_range', bracket)
            self.assertIn('rate', bracket)
            self.assertIn('taxable_amount', bracket)
            self.assertIn('tax_amount', bracket)

    def test_zero_income(self):
        """测试零收入"""
        result = self.calculator.calculate_income_tax(0, FilingStatus.SINGLE)
        self.assertEqual(result['total_tax'], 0)
        self.assertEqual(result['effective_rate'], 0)


class TestFICATax(unittest.TestCase):
    """测试FICA税"""

    def setUp(self):
        self.calculator = FederalTaxCalculator()

    def test_basic_fica(self):
        """测试基本FICA税"""
        result = self.calculator.calculate_fica_tax(50000, FilingStatus.SINGLE)
        # 社会保险税: 50000 * 0.062 = 3100
        self.assertEqual(result['social_security_tax'], 3100.00)
        # 医疗保险税: 50000 * 0.0145 = 725
        self.assertEqual(result['medicare_tax'], 725.00)
        # 总计: 3825
        self.assertEqual(result['total_fica_tax'], 3825.00)

    def test_fica_above_ss_limit(self):
        """测试超过社会保险上限的工资"""
        result = self.calculator.calculate_fica_tax(200000, FilingStatus.SINGLE)
        # 社会保险税有上限 168600
        expected_ss = 168600 * 0.062
        self.assertEqual(result['social_security_tax'], expected_ss)
        # 医疗保险税无上限
        expected_medicare = 200000 * 0.0145
        self.assertEqual(result['medicare_tax'], expected_medicare)

    def test_additional_medicare_tax(self):
        """测试附加医疗保险税"""
        # 单身超过200000触发附加税
        result = self.calculator.calculate_fica_tax(250000, FilingStatus.SINGLE)
        # 附加税: (250000 - 200000) * 0.009 = 450
        self.assertEqual(result['additional_medicare_tax'], 450.00)

    def test_married_additional_medicare(self):
        """测试已婚的附加医疗保险税"""
        # 已婚联合超过250000触发
        result = self.calculator.calculate_fica_tax(300000, FilingStatus.MARRIED_JOINTLY)
        # 附加税: (300000 - 250000) * 0.009 = 450
        self.assertEqual(result['additional_medicare_tax'], 450.00)


class TestSelfEmploymentTax(unittest.TestCase):
    """测试自雇税"""

    def setUp(self):
        self.calculator = FederalTaxCalculator()

    def test_basic_se_tax(self):
        """测试基本自雇税"""
        result = self.calculator.calculate_self_employment_tax(50000)
        # 应税收入: 50000 * 0.9235 = 46175
        self.assertEqual(result['taxable_earnings'], 46175.00)
        # 自雇税: 46175 * 0.153 ≈ 7064.78
        self.assertAlmostEqual(result['total_se_tax'], 7064.78, places=2)
        # 可扣除: 7064.78 * 0.5 = 3532.39
        self.assertAlmostEqual(result['deductible_amount'], 3532.39, places=2)

    def test_high_se_income(self):
        """测试高自雇收入"""
        result = self.calculator.calculate_self_employment_tax(200000)
        self.assertEqual(result['net_earnings'], 200000)
        # 社会保险部分有上限
        self.assertGreater(result['total_se_tax'], 0)
        # 可扣除50%
        self.assertEqual(result['deductible_amount'], result['total_se_tax'] / 2)


class TestCapitalGainsTax(unittest.TestCase):
    """测试资本利得税"""

    def setUp(self):
        self.calculator = FederalTaxCalculator()

    def test_short_term_capital_gains(self):
        """测试短期资本利得"""
        result = self.calculator.calculate_capital_gains_tax(
            10000, 50000, FilingStatus.SINGLE, "short"
        )
        self.assertEqual(result['capital_gains'], 10000)
        self.assertEqual(result['holding_period'], "short-term (≤ 1 year)")
        self.assertGreater(result['capital_gains_tax'], 0)

    def test_long_term_capital_gains_zero_rate(self):
        """测试长期资本利得0%税率"""
        # 低收入适用0%税率
        result = self.calculator.calculate_capital_gains_tax(
            10000, 30000, FilingStatus.SINGLE, "long"
        )
        self.assertEqual(result['holding_period'], "long-term (> 1 year)")
        # 应该是0%或15%税率
        self.assertIn(result['primary_tax_rate'], [0.0, 0.15])

    def test_long_term_capital_gains_15_rate(self):
        """测试长期资本利得15%税率"""
        result = self.calculator.calculate_capital_gains_tax(
            50000, 70000, FilingStatus.SINGLE, "long"
        )
        self.assertEqual(result['capital_gains'], 50000)
        # 应该适用15%税率
        self.assertEqual(result['primary_tax_rate'], 0.15)

    def test_long_term_capital_gains_20_rate(self):
        """测试长期资本利得20%税率"""
        result = self.calculator.calculate_capital_gains_tax(
            100000, 600000, FilingStatus.SINGLE, "long"
        )
        # 高收入应该适用20%税率
        self.assertEqual(result['primary_tax_rate'], 0.20)

    def test_niit_tax(self):
        """测试净投资收入税"""
        # 高收入应该触发NIIT
        result = self.calculator.calculate_capital_gains_tax(
            100000, 250000, FilingStatus.SINGLE, "long"
        )
        # 应该有NIIT
        self.assertGreater(result['net_investment_income_tax'], 0)


class TestStandardDeduction(unittest.TestCase):
    """测试标准扣除额"""

    def setUp(self):
        self.calculator = FederalTaxCalculator()

    def test_single_standard_deduction(self):
        """测试单身标准扣除"""
        result = self.calculator.calculate_standard_deduction(FilingStatus.SINGLE)
        self.assertEqual(result['base_deduction'], 14600)
        self.assertEqual(result['total_standard_deduction'], 14600)

    def test_married_jointly_standard_deduction(self):
        """测试已婚联合标准扣除"""
        result = self.calculator.calculate_standard_deduction(FilingStatus.MARRIED_JOINTLY)
        self.assertEqual(result['base_deduction'], 29200)

    def test_senior_additional_deduction(self):
        """测试老年人额外扣除"""
        # 单身65岁以上
        result = self.calculator.calculate_standard_deduction(
            FilingStatus.SINGLE,
            age_65_or_older=1
        )
        # 应该有额外扣除
        self.assertGreater(result['additional_deduction'], 0)
        self.assertGreater(result['total_standard_deduction'], result['base_deduction'])

    def test_blind_additional_deduction(self):
        """测试盲人额外扣除"""
        result = self.calculator.calculate_standard_deduction(
            FilingStatus.SINGLE,
            blind=1
        )
        self.assertGreater(result['additional_deduction'], 0)

    def test_multiple_additional_deductions(self):
        """测试多项额外扣除"""
        result = self.calculator.calculate_standard_deduction(
            FilingStatus.SINGLE,
            age_65_or_older=1,
            blind=1
        )
        # 应该有两项额外扣除
        self.assertEqual(result['additional_deduction'], 1950 * 2)


class TestTotalTaxLiability(unittest.TestCase):
    """测试综合税负计算"""

    def setUp(self):
        self.calculator = FederalTaxCalculator()

    def test_simple_w2_employee(self):
        """测试简单W-2雇员"""
        result = self.calculator.calculate_total_tax_liability(
            gross_income=75000,
            filing_status=FilingStatus.SINGLE
        )
        self.assertEqual(result['gross_income'], 75000)
        # 应该使用标准扣除
        self.assertEqual(result['deduction_type'], 'Standard')
        # 应税收入 = 75000 - 14600
        self.assertEqual(result['taxable_income'], 60400)
        self.assertGreater(result['total_tax_liability'], 0)

    def test_itemized_deductions(self):
        """测试分项扣除"""
        result = self.calculator.calculate_total_tax_liability(
            gross_income=100000,
            filing_status=FilingStatus.SINGLE,
            itemized_deductions=20000
        )
        # 应该使用分项扣除（大于标准扣除）
        self.assertEqual(result['deduction_type'], 'Itemized')
        self.assertEqual(result['deduction_amount'], 20000)

    def test_self_employed_taxpayer(self):
        """测试自雇纳税人"""
        result = self.calculator.calculate_total_tax_liability(
            gross_income=100000,
            filing_status=FilingStatus.SINGLE,
            self_employed=True
        )
        # 应该有自雇税
        self.assertGreater(result['self_employment_tax'], 0)
        # AGI应该扣除了50%自雇税
        self.assertLess(result['adjusted_gross_income'], result['gross_income'])

    def test_with_capital_gains(self):
        """测试包含资本利得"""
        result = self.calculator.calculate_total_tax_liability(
            gross_income=80000,
            filing_status=FilingStatus.SINGLE,
            capital_gains=20000
        )
        # 应该有资本利得税
        self.assertGreater(result['capital_gains_tax'], 0)

    def test_with_tax_credits(self):
        """测试税收抵免"""
        result = self.calculator.calculate_total_tax_liability(
            gross_income=60000,
            filing_status=FilingStatus.SINGLE,
            tax_credits=2000
        )
        # 税收抵免应该减少最终税负
        self.assertEqual(result['tax_credits'], 2000)
        self.assertLess(
            result['total_tax_liability'],
            result['total_tax_before_credits']
        )

    def test_married_couple_high_income(self):
        """测试已婚高收入夫妇"""
        result = self.calculator.calculate_total_tax_liability(
            gross_income=300000,
            filing_status=FilingStatus.MARRIED_JOINTLY,
            itemized_deductions=35000,
            capital_gains=50000
        )
        self.assertEqual(result['gross_income'], 300000)
        self.assertEqual(result['deduction_type'], 'Itemized')
        self.assertGreater(result['income_tax'], 0)
        self.assertGreater(result['capital_gains_tax'], 0)
        # 计算有效税率
        self.assertGreater(result['effective_tax_rate'], 0)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""

    def test_format_currency(self):
        """测试货币格式化"""
        from federal_tax import format_currency
        self.assertEqual(format_currency(1000.50), "$1,000.50")
        self.assertEqual(format_currency(1234567.89), "$1,234,567.89")

    def test_format_percentage(self):
        """测试百分比格式化"""
        from federal_tax import format_percentage
        self.assertEqual(format_percentage(12.5), "12.50%")
        self.assertEqual(format_percentage(0.15), "0.15%")


if __name__ == '__main__':
    unittest.main(verbosity=2)
