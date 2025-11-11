# 美国综合税务计算器 | US Comprehensive Tax Calculator

这是一个全面的美国税务计算工具，支持**联邦税**和**田纳西州税**的计算，帮助纳税人了解和规划税务。

## 🎯 功能概览

### 联邦税计算（Federal Taxes - 2024税年）

1. **联邦所得税** - 基于2024年税级表的累进税计算
2. **FICA税** - 社会保险税（6.2%）和医疗保险税（1.45%）
3. **自雇税** - 自由职业者和个体经营者的自雇税（15.3%）
4. **资本利得税** - 长期和短期资本利得税计算
5. **标准扣除额** - 不同报税身份的标准扣除
6. **综合税负** - 完整的联邦税务计算（包含扣除和抵免）

### 田纳西州税（Tennessee State Taxes）

田纳西州是美国税收最友好的州之一：

1. **无个人所得税** ✓ - 田纳西州不对工资收入征收州所得税
2. **销售税** - 州销售税率7%，加上地方税通常为8.5%-9.75%
3. **房产税** - 由各县和市政府征收，税率因地区而异
4. **商业税** - 企业商业税和特许经营税

### 综合功能

- **完整税负计算** - 联邦税 + 州税的综合计算
- **税务规划工具** - 比较不同报税身份、退休账户节税等
- **交互式CLI** - 友好的中英文双语命令行界面

## 安装

```bash
# 克隆仓库
git clone <repository-url>
cd cal_tax

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 快速开始 - 综合计算器

```bash
# 运行综合税务计算器（推荐）
python tax_calculator.py
```

综合计算器包含：
- 联邦税 + 州税的完整计算
- 税务规划工具
- 不同报税身份比较
- 退休账户节税计算

### 单独使用各模块

```bash
# 联邦税计算器
python federal_tax_cli.py

# 田纳西州税计算器
python tn_tax_calculator.py

# 查看联邦税示例
python federal_tax_examples.py

# 查看州税示例
python example.py
```

### 作为Python模块使用

#### 联邦税计算

```python
from federal_tax import FederalTaxCalculator, FilingStatus

calculator = FederalTaxCalculator()

# 计算联邦所得税
income_tax = calculator.calculate_income_tax(
    taxable_income=75000,
    filing_status=FilingStatus.SINGLE
)

# 计算FICA税
fica_tax = calculator.calculate_fica_tax(
    wages=85000,
    filing_status=FilingStatus.SINGLE
)

# 计算自雇税
se_tax = calculator.calculate_self_employment_tax(
    net_earnings=100000
)

# 计算资本利得税
cg_tax = calculator.calculate_capital_gains_tax(
    capital_gains=20000,
    ordinary_income=70000,
    filing_status=FilingStatus.SINGLE,
    holding_period="long"  # 长期持有
)

# 综合税负计算
total_tax = calculator.calculate_total_tax_liability(
    gross_income=100000,
    filing_status=FilingStatus.SINGLE,
    itemized_deductions=15000,
    tax_credits=2000,
    capital_gains=10000,
    self_employed=False
)
```

#### 田纳西州税计算

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
    market_value=300000,
    county="Shelby"
)

# 计算商业税
business_tax = calculator.calculate_business_tax(
    gross_receipts=500000,
    business_type="retail"
)

# 计算特许经营税
franchise_tax = calculator.calculate_franchise_tax(
    net_worth=1000000
)
```

## 📊 支持的税务类型详解

### 联邦税（2024税年）

#### 所得税税级（Income Tax Brackets）
- **Single**: 10%, 12%, 22%, 24%, 32%, 35%, 37%
- **Married Filing Jointly**: 10%, 12%, 22%, 24%, 32%, 35%, 37%
- **Head of Household**: 10%, 12%, 22%, 24%, 32%, 35%, 37%

#### 标准扣除额（Standard Deduction）
- Single: $14,600
- Married Filing Jointly: $29,200
- Head of Household: $21,900

#### FICA税率
- 社会保险税: 6.2% (工资基数上限: $168,600)
- 医疗保险税: 1.45%
- 附加医疗保险税: 0.9% (高收入者)

#### 资本利得税率
- 长期资本利得: 0%, 15%, 20% (根据收入)
- 净投资收入税: 3.8% (高收入者)

### 田纳西州税

#### 支持的县
工具包含田纳西州主要县的税率数据：
- Davidson County (纳什维尔) - 销售税 9.25%, 房产税 $3.155/$100
- Shelby County (孟菲斯) - 销售税 9.25%, 房产税 $3.49/$100
- Knox County (诺克斯维尔) - 销售税 9.25%, 房产税 $2.47/$100
- Hamilton County (查塔努加) - 销售税 9.25%, 房产税 $2.63/$100
- Rutherford, Williamson, Montgomery, Sumner等

#### 企业税类型
- Retail (零售): 0.15%
- Wholesale (批发): 0.15%
- Manufacturing (制造): 0.15%
- Service (服务): 0.25%
- Financial (金融): 0.25%
- Professional (专业服务): 0.625%

## 🧪 测试

运行测试以验证计算准确性：

```bash
# 联邦税测试
python test_federal_tax.py -v

# 田纳西州税测试
python test_tennessee_tax.py -v
```

所有测试均已通过，包括：
- 15个联邦税测试用例
- 15个田纳西州税测试用例

## 📈 使用场景示例

### 场景1: W-2雇员（年薪$90,000）
```python
# 综合税负计算
result = calculator.calculate_total_tax_liability(
    gross_income=90000,
    filing_status=FilingStatus.SINGLE
)
# 结果: 联邦所得税 + FICA税 + 州税（如有）
```

### 场景2: 自由职业者（年收入$120,000）
```python
result = calculator.calculate_total_tax_liability(
    gross_income=120000,
    filing_status=FilingStatus.SINGLE,
    self_employed=True  # 包含自雇税计算
)
```

### 场景3: 已婚夫妇（收入$150,000 + 资本利得$25,000）
```python
result = calculator.calculate_total_tax_liability(
    gross_income=150000,
    filing_status=FilingStatus.MARRIED_JOINTLY,
    capital_gains=25000,
    itemized_deductions=32000
)
```

## 🎓 税务知识

### 累进税制
美国采用累进税制，收入越高，边际税率越高。但实际税率（effective rate）通常低于最高边际税率。

### 标准扣除 vs 分项扣除
- **标准扣除**: 固定金额，简单易用
- **分项扣除**: 包括房贷利息、慈善捐款、医疗费用等，适合有大额可扣除项目的纳税人

### 田纳西州的税收优势
- ✓ 无个人所得税
- ✓ 无资本利得州税
- ✓ 相对较低的生活成本
- ✓ 对退休人员友好

## 📁 项目文件结构

```
cal_tax/
├── federal_tax.py              # 联邦税核心模块
├── federal_tax_cli.py          # 联邦税CLI界面
├── federal_tax_examples.py     # 联邦税使用示例
├── test_federal_tax.py         # 联邦税测试
├── tennessee_tax.py            # 田纳西州税核心模块
├── tn_tax_calculator.py        # 州税CLI界面
├── example.py                  # 州税使用示例
├── test_tennessee_tax.py       # 州税测试
├── tax_calculator.py           # 综合计算器（推荐使用）
├── README.md                   # 项目文档
└── requirements.txt            # 依赖文件
```

## ⚠️ 重要声明

**此工具仅供参考和教育目的。**

- 税法复杂且经常变化，实际税务情况可能因个人情况而异
- 本工具基于2024年税法数据，请以当年IRS和州政府公布的数据为准
- 实际报税时，请咨询专业税务顾问、CPA或使用IRS认证的报税软件
- 本工具不构成税务建议

## 📚 参考资料

- [IRS Official Website](https://www.irs.gov)
- [Tennessee Department of Revenue](https://www.tn.gov/revenue)
- [IRS Tax Brackets 2024](https://www.irs.gov/filing/federal-income-tax-rates-and-brackets)
- [IRS Standard Deduction](https://www.irs.gov/newsroom/irs-provides-tax-inflation-adjustments-for-tax-year-2024)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交问题报告和拉取请求！如果您发现税率数据有误或希望添加新功能，请创建issue或PR。

## 🔄 更新日志

### v2.0 (最新)
- ✨ 新增完整的美国联邦税计算功能
- ✨ 新增综合税务计算器
- ✨ 新增税务规划工具
- ✨ 支持2024税年最新税率
- ✨ 30个测试用例确保准确性

### v1.0
- ✨ 田纳西州税计算器
- ✨ 支持销售税、房产税、商业税
