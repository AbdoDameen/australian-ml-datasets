import csv
from collections import Counter

with open('raw/australian_car_market_clean.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f'Total rows: {len(rows)}')
print(f'Columns: {list(rows[0].keys())}')
print()

for col in ['brand', 'type', 'gearbox', 'fuel', 'status', 'color', 'seating_capacity']:
    vals = Counter(r[col] for r in rows)
    print(f'{col}: {len(vals)} unique, top 5: {dict(vals.most_common(5))}')

print()

for col in ['price', 'year', 'kilometers', 'cc']:
    nums = []
    for r in rows:
        try:
            nums.append(float(r[col]) if r[col].strip() else None)
        except:
            pass
    nums = [n for n in nums if n is not None]
    if nums:
        nums.sort()
        print(f'{col}: min={min(nums):.0f}, max={max(nums):.0f}, median={nums[len(nums)//2]:.0f}, mean={sum(nums)/len(nums):.0f}')

print()
for col in rows[0].keys():
    missing = sum(1 for r in rows if not r[col].strip())
    if missing:
        print(f'{col}: {missing} missing ({missing/len(rows)*100:.1f}%)')
