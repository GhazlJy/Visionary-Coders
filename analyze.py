import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

df = pd.read_csv('sample_actions.csv')

def feedback(row):
    if row['action'] == 'shot':
        if pd.isna(row['xG']) or row['xG'] < 0.1:
            return 'تسديدة ضعيفة، اقترب أكثر'
        else:
            return 'تسديدة ممتازة 👏'
    elif row['action'] == 'pass':
        if row['x'] < 0.3:
            return 'فتّح الملعب قبل التمرير'
        else:
            return 'تمريره ناجحة ✅'
    return '—'

df['feedback'] = df.apply(feedback, axis=1)
print(df[['timestamp', 'action', 'xG', 'feedback']])

pitch = Pitch()
fig, ax = pitch.draw()
pitch.scatter(df['x']*120, df['y']*80, ax=ax, color='red', s=100)
plt.title('مواقع الحركات في الملعب ⚽')
plt.show()
