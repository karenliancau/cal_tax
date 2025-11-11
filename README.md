# 田纳西州报税工具 (Tennessee Tax Calculator)

这是一个针对美国田纳西州的综合报税计算工具，支持计算田纳西州的各类税收。

## 田纳西州税收概览

田纳西州是美国税收较为友好的州之一：

- **无个人所得税**: 田纳西州不对工资收入征收州所得税
- **销售税**: 州销售税率为7%，加上地方税后通常为8.5%-9.75%
- **房产税**: 由各县和市政府征收，税率因地区而异
- **企业税**: 包括商业税(Business Tax)和特许经营税(Franchise Tax)

## 功能特性

1. **销售税计算器** - 计算商品和服务的销售税
2. **房产税计算器** - 估算房产应缴税额
3. **企业税计算器** - 计算商业税和特许经营税
4. **命令行界面** - 易于使用的交互式界面

## 安装

```bash
# 克隆仓库
git clone <repository-url>
cd cal_tax

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 命令行界面

```bash
python tn_tax_calculator.py
```

### 作为Python模块使用

```python
from tennessee_tax import TennesseeTaxCalculator

calculator = TennesseeTaxCalculator()

# 计算销售税
sales_tax = calculator.calculate_sales_tax(
    amount=100.00,
    county="Davidson"
)

# 计算房产税
property_tax = calculator.calculate_property_tax(
    assessed_value=200000,
    county="Shelby"
)

# 计算企业税
business_tax = calculator.calculate_business_tax(
    gross_receipts=500000,
    business_type="retail"
)
```

## 支持的县

工具包含田纳西州主要县的税率数据：
- Davidson County (纳什维尔)
- Shelby County (孟菲斯)
- Knox County (诺克斯维尔)
- Hamilton County (查塔努加)
- 等等...

## 注意事项

⚠️ 此工具仅供参考和教育目的。实际报税时请咨询专业税务顾问或会计师。税率和法规可能会变化。

## 许可证

MIT License

## 贡献

欢迎提交问题报告和拉取请求！
