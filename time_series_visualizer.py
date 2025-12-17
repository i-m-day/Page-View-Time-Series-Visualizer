import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col="date", parse_dates=True)
df = df.rename(columns={"value":"page_views"})


# Clean data
df = df[(
    (df["page_views"] > df["page_views"].quantile(0.025)) &
    (df["page_views"] < df["page_views"].quantile(0.975)))]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(12, 6))    
    plt.plot(df.index, df['page_views'])
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    # df_bar = df_bar.groupby(['year','month'], sort=False).mean().reset_index()
    df_pivot = df_bar.groupby(['year', 'month'])['page_views'].mean().unstack()

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_pivot = df_pivot[month_order]    # df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Draw bar plot
    # fig = plt.figure(figsize=(12, 6))
    # sns.barplot(data=df_bar, x='year', y='page_views', hue='month', hue_order=month_order)
    fig = df_pivot.plot(kind='bar', figsize=(15, 10)).get_figure()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=month_order)


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    sns.boxplot(x="year", y="page_views", data=df_box, ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)
    sns.boxplot(x="month", y="page_views", data=df_box.sort_values('month'), ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
