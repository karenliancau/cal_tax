"""
田纳西州税务计算器测试
Tennessee Tax Calculator Tests
"""

import unittest
from tennessee_tax import TennesseeTaxCalculator


class TestTennesseeTaxCalculator(unittest.TestCase):
    """测试田纳西州税务计算器"""

    def setUp(self):
        """设置测试"""
        self.calculator = TennesseeTaxCalculator()

    def test_sales_tax_basic(self):
        """测试基本销售税计算"""
        result = self.calculator.calculate_sales_tax(100.00, "Davidson")
        self.assertEqual(result['amount'], 100.00)
        self.assertEqual(result['tax_rate'], 0.0925)
        self.assertEqual(result['tax_amount'], 9.25)
        self.assertEqual(result['total'], 109.25)

    def test_sales_tax_different_counties(self):
        """测试不同县的销售税"""
        # Davidson County
        result1 = self.calculator.calculate_sales_tax(100.00, "Davidson")
        self.assertEqual(result1['tax_amount'], 9.25)

        # Rutherford County (更高税率)
        result2 = self.calculator.calculate_sales_tax(100.00, "Rutherford")
        self.assertEqual(result2['tax_amount'], 9.75)

    def test_sales_tax_default(self):
        """测试默认销售税率"""
        result = self.calculator.calculate_sales_tax(100.00)
        self.assertEqual(result['tax_rate'], 0.09)
        self.assertEqual(result['tax_amount'], 9.00)

    def test_property_tax_basic(self):
        """测试基本房产税计算"""
        result = self.calculator.calculate_property_tax(200000, "Davidson")
        # 市场价值 200,000 * 25% = 50,000 评估价值
        # (50,000 / 100) * 3.155 = 1,577.50
        self.assertEqual(result['market_value'], 200000)
        self.assertEqual(result['assessed_value'], 50000)
        self.assertEqual(result['annual_tax'], 1577.50)

    def test_property_tax_different_counties(self):
        """测试不同县的房产税"""
        market_value = 300000

        # Knox County (较低税率)
        result1 = self.calculator.calculate_property_tax(market_value, "Knox")
        # (300,000 * 0.25 / 100) * 2.47 = 1,852.50
        self.assertEqual(result1['annual_tax'], 1852.50)

        # Shelby County (较高税率)
        result2 = self.calculator.calculate_property_tax(market_value, "Shelby")
        # (300,000 * 0.25 / 100) * 3.49 = 2,617.50
        self.assertEqual(result2['annual_tax'], 2617.50)

    def test_business_tax_retail(self):
        """测试零售商业税"""
        result = self.calculator.calculate_business_tax(500000, "retail")
        # 500,000 * 0.0015 = 750
        self.assertEqual(result['gross_receipts'], 500000)
        self.assertEqual(result['tax_amount'], 750.00)

    def test_business_tax_professional(self):
        """测试专业服务商业税"""
        result = self.calculator.calculate_business_tax(200000, "professional")
        # 200,000 * 0.00625 = 1,250
        self.assertEqual(result['tax_amount'], 1250.00)

    def test_franchise_tax_basic(self):
        """测试基本特许经营税"""
        result = self.calculator.calculate_franchise_tax(1000000)
        # 1,000,000 * 0.0025 = 2,500
        self.assertEqual(result['net_worth'], 1000000)
        self.assertEqual(result['tax_amount'], 2500.00)

    def test_franchise_tax_minimum(self):
        """测试特许经营税最低税额"""
        # 净资产很小的情况
        result = self.calculator.calculate_franchise_tax(10000)
        # 10,000 * 0.0025 = 25，但最低为100
        self.assertEqual(result['tax_amount'], 100.00)

    def test_get_available_counties(self):
        """测试获取县列表"""
        counties = self.calculator.get_available_counties()
        self.assertIn("Davidson", counties)
        self.assertIn("Shelby", counties)
        self.assertIn("Knox", counties)
        self.assertNotIn("default", counties)

    def test_get_available_business_types(self):
        """测试获取企业类型列表"""
        types = self.calculator.get_available_business_types()
        self.assertIn("retail", types)
        self.assertIn("professional", types)
        self.assertIn("service", types)
        self.assertNotIn("default", types)

    def test_decimal_precision(self):
        """测试小数精度"""
        # 测试需要四舍五入的情况
        result = self.calculator.calculate_sales_tax(10.01, "Davidson")
        # 10.01 * 0.0925 = 0.925925，应该四舍五入为 0.93
        self.assertEqual(result['tax_amount'], 0.93)

    def test_large_amounts(self):
        """测试大额计算"""
        # 测试百万级别的金额
        result = self.calculator.calculate_property_tax(5000000, "Davidson")
        # (5,000,000 * 0.25 / 100) * 3.155 = 39,437.50
        self.assertEqual(result['annual_tax'], 39437.50)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""

    def test_format_currency(self):
        """测试货币格式化"""
        from tennessee_tax import format_currency
        self.assertEqual(format_currency(1000.50), "$1,000.50")
        self.assertEqual(format_currency(100), "$100.00")
        self.assertEqual(format_currency(1234567.89), "$1,234,567.89")

    def test_format_percentage(self):
        """测试百分比格式化"""
        from tennessee_tax import format_percentage
        self.assertEqual(format_percentage(0.0925), "9.25%")
        self.assertEqual(format_percentage(0.10), "10.00%")
        self.assertEqual(format_percentage(0.005), "0.50%")


if __name__ == '__main__':
    unittest.main()
