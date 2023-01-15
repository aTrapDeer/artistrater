import streamlit as st
import requests
from bs4 import BeautifulSoup
import billboard
from pytrends.request import TrendReq

def main():
    st.title("Artist Relevancy Checker")

    #Ask user to input the artist's name
    artist = st.text_input("Enter an artist name: ")

    if st.button("Search"):
        search_artist(artist)

def search_artist(artist):
    # Use the Billboard Music API to get the artist's ranking on the Billboard charts
    chart = billboard.ChartData('hot-100')

    # Create a variable to keep track of the billboard bonus value
    bonus = 0

    # Create a list to store the artist's entries on the Billboard chart
    artist_entries = []

    # Extract the artist's ranking and add bonus based on it from the API response
    for i in range(len(chart)):
        if artist.lower() in chart[i].artist.lower():
            if chart[i].title not in artist_entries:
                artist_entries.append(f'{chart[i].rank} - {chart[i].title}')
                bonus += 40 - (.01 * i)

    # Use the Google Trends API to get the artist's search interest over time
    pytrends = TrendReq()
    pytrends.build_payload([artist], cat=0, timeframe='today 12-m', geo='', gprop='')
    artist_interest = pytrends.interest_over_time()[artist]

    #Calculate the average trend score
    average_trend_score = artist_interest.mean()

    # Create a relevancy value
    relevancy = 0
    trend_bonus = 0 

    #Adds the Billboard bonus to relevancy
    relevancy += bonus

    #Create a flag variable to check if relevancy was added
    flag = 0

    # Boost the relevancy if the artist has a high google trend score. Add value based on score rating.
    if average_trend_score > 60 and flag == 0:
        trend_bonus = 150
        relevancy += trend_bonus
        flag = 1
    elif average_trend_score > 30 and flag == 0:
        trend_bonus = 80
        relevancy += trend_bonus
        flag = 1
    elif average_trend_score > 20 and flag ==0:
        trend_bonus = 50
        relevancy += trend_bonus
        flag = 1
    elif average_trend_score > 10 and flag == 0:
        trend_bonus = 30
        relevancy += trend_bonus
        flag = 1
    else:
        relevancy += trend_bonus

    # Print the artist's entries on the Billboard chart
    if artist_entries:
        st.write(f'{artist} has the following entries on the Billboard chart:')
        for entry in artist_entries:
            st.write(entry)
    else:
        st.write(f'{artist} has no entries on the Billboard chart.')

    artist = artist.lower()
    artist = artist.replace(" ", "-")
    #Get TikTok views for artist

    url = f"https://www.tiktok.com/discover/{artist}-sounds?lang=en"
   
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    total_views_element = soup.select_one("h2.tiktok-hvuiar-H2Info-StyledViews")

    try:
        total_views_string = total_views_element.text
        total_views_string = total_views_string.replace(" views","")
        # check if the last character is "B"
        if total_views_string[-1] == "B":
            total_views = float(total_views_string[:-1]) * 1000000000
        elif total_views_string[-1] == "M":
            total_views = float(total_views_string[:-1]) * 1000000
        elif total_views_string[-1] == "K":
            total_views = float(total_views_string[:-1]) * 1000
        else:
            total_views = float(total_views_string)

        #Create a flag variable to check if tiktok score was added
        flag2 = 0
        
    except:
        total_views = 0
        flag2 = 0
    else:
        # Create a TikTok score
        tiktok_score = 0

    if total_views > 100000000 and flag2 == 0:
        tiktok_score = 150
        relevancy += tiktok_score
        flag2 = 1
    elif total_views > 50000000 and flag2 == 0:
        tiktok_score = 80
        relevancy += tiktok_score
        flag2 = 1
    elif total_views > 10000000 and flag2 == 0:
        tiktok_score = 50
        relevancy += tiktok_score
        flag2 = 1
    elif total_views > 1000000 and flag2 == 0:
        tiktok_score = 30
        relevancy += tiktok_score
        flag2 = 1
    else:
        tiktok_score = 0
        relevancy += tiktok_score 

    st.write(f'The relevancy score for {artist} is: {relevancy}')
    
    st.write(f'Breakdown of Relevancy score:')
    
    st.write(f'- Billboard Bonus: {bonus}')
    
    st.write(f'- Google Trends Bonus: {trend_bonus}')
    
    st.write(f'- TikTok Bonus: {tiktok_score}')

            #Check if the artist is relevant
    if relevancy >= 500:
            st.write(f'This artist is currently SUPER hot, relevant AND established. Extremely oversaturated. Probably dominating the charts.')
    elif relevancy > 280:
            st.write(f'This artist is hot and relevant right now, and probably established - or is a legacy act. Probably oversaturated, and hitting the charts.')
    elif relevancy > 190:
            st.write(f'This artist is hot and relevant right now. Possibly still underground, good opportunity to produce and build content around. They may be on the Billboard charts too, if not soon.')
    elif relevancy > 150:
            st.write(f'This artist might be relevant soon, or was recently relevant. Perfect opportunity to get ahead.')
    elif relevancy > 100:
            st.write(f'This artist might see mainstream success in the future. You might be a bit early for this artist.')
    elif relevancy > 70:
                st.write(f'This artist is really underground, might be a bit early to tell for certain. You are early for this artist.')
    elif relevancy > 10:
            st.write(f'This artist is really underground, early to tell for certain of relevancy. You are FOR SURE early for this artist.')
    else:
            st.write(f'This artist isnt established or relevant AT ALL. Or check their name spelling. This artist might not have had much press, sales or trends relating around them recently.')

if __name__ == '__main__':
    main()

