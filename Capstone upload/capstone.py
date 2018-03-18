# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 10:56:55 2018

@author: vg809d
"""
from codecademySQL import sql_query
import pandas as pd
from matplotlib import pyplot as plt
#import scipy

# Examine visits
sql_query('''
Select * 
from visits
limit 5          
''')
#Examine fitness_tests
sql_query('''
Select * 
from fitness_tests
limit 5          
''')
#Examine applications
sql_query('''
Select * 
from applications
limit 5          
''')
#Examine purchases
sql_query('''
Select * 
from purchases
limit 5          
''')

df = sql_query('''
          
select
    visits.first_name, visits.last_name, visits.gender,visits.email,
    visits.visit_date, fitness_tests.fitness_test_date,
    applications.application_date, purchases.purchase_date
from visits
left join fitness_tests
    on visits.first_name = fitness_tests.first_name
    and visits.last_name = fitness_tests.last_name
    and visits.email = fitness_tests.email
left join applications
    on visits.first_name = applications.first_name
    and visits.last_name = applications.last_name
    and visits.email = applications.email
left join purchases
    on visits.first_name = purchases.first_name
    and visits.last_name = purchases.last_name
    and visits.email = purchases.email
Where visits.visit_date >= '7-1-17'

          ''')

df['ab_test_group'] = df.fitness_test_date.apply(lambda x:
                                                'A' if pd.notnull(x) else 'B')
    

ab_counts = df.groupby('ab_test_group').email.count().reset_index()

plt.pie(ab_counts.email, autopct='%d%%',labels=['A','B'])
plt.axis('equal')
plt.show()
plt.savefig('ab_test_pie_chart.png')

df['is_application']=df.application_date.apply(lambda x: "Application" if pd.notnull(x) else 'No Application')

app_counts=df.groupby(['ab_test_group', 'is_application']).email.count().reset_index()



app_pivot=app_counts.pivot(
columns='is_application',
index='ab_test_group',
values = 'email').reset_index()

app_pivot['Total']=app_pivot.Application + app_pivot['No Application']
app_pivot['Percent with Application']=\
app_pivot.Application/app_pivot.Total

print(app_pivot)
from scipy.stats import chi2_contingency
X = [[250, 2254], [325, 2175]]
chi2, pval, dof, expected = chi2_contingency(X)
print (pval)
# P value less than 0.00095 the difference isn't statistically significant

df['is_member']=df.purchase_date.apply(lambda x: 'Member' if pd.notnull(x) else \
  "Not Member")
just_apps=df[df.is_application != 'No Application']
just_app_count=just_apps.groupby(['is_member','ab_test_group']).first_name.count().reset_index()
just_app_count_pivot=just_app_count.pivot(
        columns='is_member',
        index='ab_test_group',
        values='first_name').reset_index()
member_pivot=just_app_count_pivot

member_pivot['Total']=(member_pivot.Member + member_pivot['Not Member'])
member_pivot['Percent Membership']=member_pivot.Member/member_pivot.Total
print (member_pivot)

X2 = [[200, 50], [250, 75]]
chi2, pval2, dof, expected=chi2_contingency(X2)
print(pval2)

final_member_count = df.groupby(['ab_test_group', 'is_member'])\
                 .first_name.count().reset_index()
final_member_pivot = final_member_count.pivot(columns='is_member',
                                  index='ab_test_group',
                                  values='first_name')\
                           .reset_index()

final_member_pivot['Total'] = final_member_pivot.Member + final_member_pivot['Not Member']
final_member_pivot['Percent Purchase'] = final_member_pivot.Member / final_member_pivot.Total
print(final_member_pivot)

X3 = [[200, 2304], [250, 2250]]
chi2, pval3, dof, expected=chi2_contingency(X3)
print(pval3)
# Percent of Visitors who Apply
ax = plt.subplot()
plt.bar(range(len(app_pivot)),
       app_pivot['Percent with Application'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.show()
plt.savefig('percentage of visitors who apply.png')

# Percent of Applicants who Purchase
ax = plt.subplot()
plt.bar(range(len(member_pivot)),
       member_pivot['Percent Membership'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
plt.show()
plt.savefig('percentage of applicants to purchase.png')

# Percent of Visitors who Purchase
ax = plt.subplot()
plt.bar(range(len(final_member_pivot)),
       final_member_pivot['Percent Purchase'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.show()
plt.savefig('percentage of visitors who purchase.png')