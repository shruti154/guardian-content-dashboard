import pandas as pd
import matplotlib.pyplot as plt
import ast

df = pd.read_csv("guardian_articles.csv")

# Convert publication date
df["webPublicationDate"] = pd.to_datetime(df["webPublicationDate"])
df["hour"] = df["webPublicationDate"].dt.hour
df["day_of_week"] = df["webPublicationDate"].dt.day_name()


# Extract wordcount from the fields column
def extract_wordcount(field):
    try:
        d = ast.literal_eval(field)
        return int(d.get("wordcount", 0))
    except:
        return 0

df["wordcount"] = df["fields"].apply(extract_wordcount)

# Remove zeros (articles with no wordcount data)
df_words = df[df["wordcount"] > 0]

# --- CHART 1: Average word count by section ---
plt.figure(figsize=(10, 5))
df_words.groupby("sectionName")["wordcount"].mean().sort_values().plot(
    kind="bar", color="steelblue"
)
plt.title("Average Word Count by Section")
plt.xlabel("Section")
plt.ylabel("Average Word Count")
plt.tight_layout()
plt.savefig("chart_wordcount.png")
plt.close()
print("Saved chart_wordcount.png")

# --- CHART 2: Publishing hours ---
plt.figure(figsize=(12, 5))
df["hour"].value_counts().sort_index().plot(kind="bar", color="coral")
plt.title("Guardian Articles Published by Hour of Day")
plt.xlabel("Hour (UTC)")
plt.ylabel("Number of Articles")
plt.tight_layout()
plt.savefig("chart_publish_hours.png")
plt.close()
print("Saved chart_publish_hours.png")

print("\nAverage word counts:")
print(df_words.groupby("sectionName")["wordcount"].mean().sort_values())

# --- CHART 3: Publishing by day of week ---
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
plt.figure(figsize=(10, 5))
df["day_of_week"].value_counts().reindex(days_order).plot(kind="bar", color="mediumpurple")
plt.title("Guardian Articles Published by Day of Week")
plt.xlabel("Day")
plt.ylabel("Number of Articles")
plt.tight_layout()
plt.savefig("chart_day_of_week.png")
plt.close()
print("Saved chart_day_of_week.png")