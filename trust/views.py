from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    HomeBannerView, LatestNewsView, AreaOfWork, Topic,
    DonationCategory, DonationAmount,
    Campaign, CampaignDonationAmount,
    Donation, AboutUs, MediaItem, ImpactCategory, TenderNotice, Stat, Trustee,
    Campaign, DonationCategory, Donation
)

# -----------------------
# Home page
# -----------------------
def home(request):
    homebanner = HomeBannerView.objects.all()
    latestnews = LatestNewsView.objects.all()
    areas = AreaOfWork.objects.all()
    return render(request, 'trust/home.html', {
        'homebanner': homebanner,
        'latestnews': latestnews,
        'areas': areas,
    })


# -----------------------
# News / Areas / Topics
# -----------------------
def latestnews_detail(request, slug):
    news = get_object_or_404(LatestNewsView, slug=slug)
    return render(request, 'trust/latestnews_detail.html', {'news': news})


def area_detail(request, slug):
    area = get_object_or_404(AreaOfWork, slug=slug)
    return render(request, "trust/area_detail.html", {"area": area})


def topic_detail(request, area_slug, topic_slug):
    topic = get_object_or_404(Topic, area__slug=area_slug, slug=topic_slug)
    return render(request, "trust/topic_detail.html", {"topic": topic})


# -----------------------
# How to Help (Donation Categories)
# -----------------------
def how_to_help(request, category=None):
    categories = DonationCategory.objects.all()
    selected_category = None
    amounts = None

    if categories.exists():
        if category:
            selected_category = get_object_or_404(DonationCategory, slug=category)
        else:
            selected_category = categories.first()
        if selected_category:
            amounts = selected_category.amounts.all()

    return render(request, "trust/how_to_help.html", {
        "categories": categories,
        "selected_category": selected_category,
        "amounts": amounts,
    })


# -----------------------
# Campaigns
# -----------------------
def campaign_list(request):
    campaigns = Campaign.objects.all().order_by("-id")
    return render(request, "trust/campaign_list.html", {"campaigns": campaigns})


def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    donation_options = campaign.donation_amounts.all()  # Related name in CampaignDonationAmount
    return render(request, "trust/campaign_detail.html", {
        "campaign": campaign,
        "donation_options": donation_options,
    })


# -----------------------
# Unified Donation Form
# -----------------------
def donation_form(request, slug=None, category_slug=None):
    campaign = None
    category = None
    donation_options = []

    if slug:
        campaign = get_object_or_404(Campaign, slug=slug)
        donation_options = campaign.donation_amounts.all()
    elif category_slug:
        category = get_object_or_404(DonationCategory, slug=category_slug)
        donation_options = category.amounts.all()
    else:
        return redirect('home')

    # Get pre-selected amount from query string
    preselected_amount = request.GET.get('amount', None)

    if request.method == "POST":
        amount_str = request.POST.get('amount', '').strip()
        if not amount_str:
            # fallback to preselected amount if not in POST
            amount_str = preselected_amount

        try:
            amount = Decimal(amount_str)
        except (InvalidOperation, TypeError):
            return render(request, 'trust/donation_form.html', {
                'campaign': campaign,
                'category': category,
                'donation_options': donation_options,
                'error': "Invalid donation amount.",
                'preselected_amount': amount_str
            })

        Donation.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            dob=request.POST.get('dob') or None,
            certificate_80g=request.POST.get('certificate_80g') == 'on',
            amount=amount,
            campaign=campaign,
            category=category,
        )
        return redirect('donation_success')

    return render(request, 'trust/donation_form.html', {
        'campaign': campaign,
        'category': category,
        'donation_options': donation_options,
        'preselected_amount': preselected_amount,
    })


def donation_success(request):
    return render(request, 'trust/donation_success.html')


# -----------------------
# About Us / Trustees
# -----------------------
def about_us(request):
    about = AboutUs.objects.first()
    stats = Stat.objects.all()
    return render(request, "trust/about_us.html", {"about": about, "stats": stats})


def board_of_trustees(request):
    trustees = Trustee.objects.all()
    return render(request, "trust/board_of_trustees.html", {"trustees": trustees})


# -----------------------
# Media
# -----------------------
def media(request):
    images = MediaItem.objects.filter(image__isnull=False).exclude(image="")
    videos = MediaItem.objects.filter(video__isnull=False).exclude(video="")
    return render(request, 'trust/media.html', {
        'images': images,
        'videos': videos,
    })


# -----------------------
# Impact Stories
# -----------------------
def impact_categories(request):
    categories = ImpactCategory.objects.all()
    return render(request, "trust/impact_categories.html", {"categories": categories})


def impact_category_detail(request, slug):
    category = get_object_or_404(ImpactCategory, slug=slug)
    stories = category.stories.all()
    return render(request, "trust/impact_category_detail.html", {
        "category": category,
        "stories": stories,
    })


# -----------------------
# Tenders
# -----------------------
def tender_notice_list(request):
    tenders = TenderNotice.objects.filter(is_active=True).order_by("-published_date")
    return render(request, "trust/tender_notice_list.html", {"tenders": tenders})
