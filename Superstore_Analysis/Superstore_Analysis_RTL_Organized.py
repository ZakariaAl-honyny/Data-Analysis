import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------- قراءة البيانات ----------
SuperstoreData = pd.read_csv("SampleSuperstore.csv", encoding='cp1252')

# عرض أول 5 صفوف
print("أول 5 صفوف:")
print(SuperstoreData.head())

# ---------- معلومات عامة والتحقق من القيم المفقودة ----------
print("\nمعلومات عن الإطار:")
SuperstoreData.info()
print("\nملخص القيم المفقودة لكل عمود:")
print(SuperstoreData.isnull().sum())

# حذف الصفوف التي تحتوي على قيم ناقصة)
SuperstoreData.dropna(inplace=True)
print("\nبعد حذف القيم الفارغة، الأبعاد:", SuperstoreData.shape)

# ---------- تحويل الأنواع ----------
SuperstoreData['Order Date'] = pd.to_datetime(SuperstoreData['Order Date'])
SuperstoreData['Ship Date'] = pd.to_datetime(SuperstoreData['Ship Date'])
SuperstoreData['Sales'] = pd.to_numeric(SuperstoreData['Sales'], errors='coerce')
SuperstoreData['Profit'] = pd.to_numeric(SuperstoreData['Profit'], errors='coerce')

print("\nالوصف الإحصائي:")
print(SuperstoreData.describe())

# ---------- تحليلات أساسية ----------
# إجمالي المبيعات لكل فئة Category
sales_by_category = SuperstoreData.groupby('Category')['Sales'].sum()
print("\nإجمالي المبيعات لكل فئة:")
print(sales_by_category)

# عدد كل نوع فئة (لرسم شريطي أفقي)
category_counts = SuperstoreData['Category'].value_counts()
print("\nعدد أنواع الفئات:")
print(category_counts)

# متوسط الربح لكل منطقة Region
region_profit_mean = SuperstoreData.groupby('Region')['Profit'].mean()
print("\nمتوسط الربح لكل منطقة:")
print(region_profit_mean)

# إجمالي المبيعات لكل عميل وتصنيفهم
customer_sales = SuperstoreData.groupby('Customer Name')['Sales'].sum()

def classify_customer(sales):
    if sales <= 1000:
        return 'صغير'
    elif sales <= 5000:
        return 'متوسط'
    else:
        return 'كبير'
    
customer_category_alt2 = customer_sales.apply(classify_customer)
customer_category_alt2.value_counts()

# وصف أعمدة Quantity و Profit
print("\nالوصف الإحصائي لأعمدة Quantity و Profit:")
print(SuperstoreData[['Quantity', 'Profit']].describe())

# تحليل أداء الفروع Segment
print("\nمتوسط المبيعات والربح لكل Segment:")
segment_analysis = SuperstoreData.groupby('Segment')[['Sales', 'Profit']].mean()
print(segment_analysis)

# ---------- رسوم بيانية وحفظها كصور ----------
# رسم شريطي لإجمالي المبيعات لكل فئة 1
plt.figure()
sales_by_category.plot(kind='bar')
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Sales')
plt.tight_layout()
plt.savefig('sales_by_category.png')  # حفظ الرسم
# plt.show()
plt.close()

# 2 مخطط دائري لنسبة المبيعات حسب المنطقة
region_sales = SuperstoreData.groupby('Region')['Sales'].sum()
plt.figure()
region_sales.plot(kind='pie', autopct='%1.1f%%')
plt.title('Sales Percentage by Region')
plt.tight_layout()
plt.savefig('region_sales.png')
# plt.show()
plt.close()

    # 3 رسم تبعثر يوضح العلاقة بين الكمية والربح
plt.figure()
plt.scatter(SuperstoreData['Quantity'], SuperstoreData['Profit'])
plt.title('Relationship Between Quantity and Profit')
plt.xlabel('Quantity')
plt.ylabel('Profit')
plt.tight_layout()
plt.savefig('quantity_vs_profit.png')
plt.close()

# 4) مخطط خطي لتطور المبيعات عبر الوقت
sales_over_time = SuperstoreData.groupby('Order Date')['Sales'].sum()
plt.figure()
plt.plot(sales_over_time.index, sales_over_time.values)
plt.title('Sales Trend Over Time')
plt.xlabel('Order Date')
plt.ylabel('Sales')
plt.tight_layout()
plt.savefig('sales_over_time.png')
# plt.show()
plt.close()

# 5 مخطط شريطي أفقي للفئة الاكثر مبيعا
plt.figure()
plt.barh(category_counts.index, category_counts.values)
plt.title('Number of The Most Ordering Category')
plt.xlabel('The Most Ordering Category')
plt.ylabel('Category Types')
plt.tight_layout()
plt.savefig('the_Most_saling_category.png')
# plt.show()
plt.close()

print("\nتحليل مكتمل. وتم حفظ الرسوم")
