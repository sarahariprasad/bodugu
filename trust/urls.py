from django.urls import path
from . import views

urlpatterns = [
    # -----------------------
    # Home & Media
    # -----------------------
    path("", views.home, name="home"),
    path("media/", views.media, name="media"),

    # -----------------------
    # Tender Notices
    # -----------------------
    path("tender-notice/", views.tender_notice_list, name="tender_notice_list"),

    # -----------------------
    # News
    # -----------------------
    path("news/<slug:slug>/", views.latestnews_detail, name="latestnews_detail"),

    # -----------------------
    # Areas & Topics
    # -----------------------
    path("areas/<slug:slug>/", views.area_detail, name="area_detail"),
    path("areas/<slug:area_slug>/<slug:topic_slug>/", views.topic_detail, name="topic_detail"),

    # -----------------------
    # Donations
    # -----------------------
    path("how-to-help/", views.how_to_help, name="how_to_help"),  
    path("how-to-help/<slug:category_slug>/", views.donation_form, name="donation_category"),  # Category donation
    path("donate/<slug:slug>/", views.donation_form, name="donation_form"),  # Campaign donation
    path("success/", views.donation_success, name="donation_success"),


    # -----------------------
    # About & Trustees
    # -----------------------
    path("about-us/", views.about_us, name="about_us"),
    path("board-of-trustees/", views.board_of_trustees, name="board_of_trustees"),

    # -----------------------
    # Impact Stories
    # -----------------------
    path("impact-stories/", views.impact_categories, name="impact_categories"),
    path("impact-stories/<slug:slug>/", views.impact_category_detail, name="impact_category_detail"),

    # -----------------------
    # Campaigns
    # -----------------------
    path("campaigns/", views.campaign_list, name="campaign_list"),
    path("campaigns/<slug:slug>/", views.campaign_detail, name="campaign_detail"),
]