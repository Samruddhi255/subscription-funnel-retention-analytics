from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; DATA,OUT,IMG=ROOT/'data',ROOT/'reports',ROOT/'images'
OUT.mkdir(exist_ok=True); IMG.mkdir(exist_ok=True)
o=pd.read_csv(DATA/'orders.csv',parse_dates=['order_date','delivery_date'])
s=pd.read_csv(DATA/'suppliers.csv')
pd.DataFrame([['orders_rows',len(o)],['duplicate_order_ids',o.order_id.duplicated().sum()],['unknown_supplier_ids',(~o.supplier_id.isin(s.supplier_id)).sum()],['negative_quantity_rows',(o.quantity<0).sum()]],columns=['check','value']).to_csv(OUT/'data_quality_checks.csv',index=False)
d=o[o.order_status=='Delivered'].copy()
overall=pd.DataFrame([{'total_orders':len(o),'delivered_orders':len(d),'revenue_inr':round(o.revenue_inr.sum(),2),'gross_profit_before_shipping_inr':round(o.gross_profit_before_shipping_inr.sum(),2),'shipping_cost_inr':round(o.shipping_cost_inr.sum(),2),'on_time_delivery_rate_pct':round((d.late_delivery==0).mean()*100,2),'late_delivery_rate_pct':round(d.late_delivery.mean()*100,2),'avg_actual_delivery_days':round(d.actual_delivery_days.mean(),2)}])
overall.to_csv(OUT/'overall_kpis.csv',index=False)
def grouped(col):
 x=d.groupby(col).agg(orders=('order_id','nunique'),revenue_inr=('revenue_inr','sum'),gross_profit_before_shipping_inr=('gross_profit_before_shipping_inr','sum'),shipping_cost_inr=('shipping_cost_inr','sum'),avg_delivery_days=('actual_delivery_days','mean'),late_orders=('late_delivery','sum'),avg_delay_days=('delay_days','mean')).reset_index()
 x['late_rate_pct']=(x.late_orders/x.orders*100).round(2); x['on_time_rate_pct']=(100-x.late_rate_pct).round(2)
 return x.round(2).sort_values('late_rate_pct',ascending=False)
for col,file in [('region','region_performance.csv'),('shipping_mode','shipping_mode_performance.csv'),('category','category_performance.csv')]:
 grouped(col).to_csv(OUT/file,index=False)
sp=d.groupby('supplier_id').agg(orders=('order_id','nunique'),late_orders=('late_delivery','sum'),avg_delay_days=('delay_days','mean'),revenue_inr=('revenue_inr','sum')).reset_index().merge(s,on='supplier_id',how='left')
sp['on_time_rate_pct']=(100-sp.late_orders/sp.orders*100).round(2); sp['target_gap_pp']=(sp.on_time_rate_pct-sp.on_time_target_pct).round(2)
sp.round(2).sort_values('target_gap_pp').to_csv(OUT/'supplier_scorecard.csv',index=False)
m=o.assign(order_month=o.order_date.dt.to_period('M').astype(str)).groupby('order_month').agg(orders=('order_id','nunique'),revenue_inr=('revenue_inr','sum'),gross_profit_before_shipping_inr=('gross_profit_before_shipping_inr','sum'),shipping_cost_inr=('shipping_cost_inr','sum'),late_rate_pct=('late_delivery','mean')).reset_index()
m['late_rate_pct']=(m.late_rate_pct*100).round(2); m.to_csv(OUT/'monthly_trends.csv',index=False)
r=grouped('region').sort_values('late_rate_pct')
plt.figure(figsize=(7,4)); plt.barh(r.region,r.late_rate_pct); plt.title('Late Delivery Rate by Region'); plt.xlabel('%'); plt.tight_layout(); plt.savefig(IMG/'late_rate_by_region.png',dpi=150); plt.close()
sm=grouped('shipping_mode')
plt.figure(figsize=(7,4)); plt.bar(sm.shipping_mode,sm.shipping_cost_inr/sm.orders); plt.title('Average Shipping Cost per Order'); plt.ylabel('INR'); plt.tight_layout(); plt.savefig(IMG/'shipping_cost_by_mode.png',dpi=150); plt.close()
top=sp.sort_values('target_gap_pp').head(10).sort_values('target_gap_pp',ascending=False)
plt.figure(figsize=(7,4)); plt.barh(top.supplier_id,top.target_gap_pp); plt.axvline(0,linewidth=1); plt.title('Supplier On-Time Rate vs Target'); plt.xlabel('Percentage-point gap'); plt.tight_layout(); plt.savefig(IMG/'supplier_target_gap.png',dpi=150); plt.close()
(OUT/'findings_and_recommendations.md').write_text('''# Findings and Recommendations\n\nReview suppliers with the largest negative target gap, accounting for order volume. Investigate regions with higher late rates and compare shipping-mode cost with service levels. Monitor revenue and gross profit together; revenue alone is not profitability.\n\n**Limitations:** data is synthetic; shipping mode is not randomly assigned; gross profit is before shipping cost; differences are descriptive rather than causal.\n''')
print('Wrote KPI tables and charts.')
