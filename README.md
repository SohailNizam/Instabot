# Instabot
A bot that takes a list of hashtags  and cycles through them following the top posters under each and liking their photos.
Number of hashtags, number of users to follow per hashtag, and number of photos to like per user can be changed.

At the end of each cycle, the new users followed and the current date are stored in a pandas df and exported to excel.

TODO:
Add a feature to go through the current excel spreadsheet and unfollow those we've followed for >= 3 days.
