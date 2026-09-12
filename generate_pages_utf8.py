import os

base_dir = r"c:\Users\Nisha Singh\build in mumbai\templates\public"

founders_html = '''{% extends "base.html" %}
{% block title %}- Founders{% endblock %}
{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
    <div class="max-w-3xl mb-24">
        <h1 class="text-5xl md:text-7xl font-heading text-white uppercase tracking-tight mb-6">The Architects<br>of the Network</h1>
        <p class="text-gray-400 text-lg">Meet the visionaries, builders, and creators behind the city's next generation of companies.</p>
    </div>

    <div class="space-y-32">
        {% for founder in founders %}
        <div class="flex flex-col md:flex-row items-center gap-16 {% if loop.index0 % 2 != 0 %}md:flex-row-reverse{% endif %}">
            <div class="w-full md:w-1/2">
                {% if founder.image_filename %}
                <img src="{{ url_for('static', filename='uploads/founders/' + founder.image_filename) }}" class="w-full h-[500px] object-cover rounded-sm grayscale hover:grayscale-0 transition duration-500">
                {% else %}
                <div class="w-full h-[500px] bg-gray-800 flex items-center justify-center text-gray-500 rounded-sm">No Image</div>
                {% endif %}
            </div>
            <div class="w-full md:w-1/2">
                <div class="mb-6 space-x-2">
                    <span class="text-[10px] font-bold uppercase tracking-wider text-primary border border-primary/30 px-2 py-1 rounded">FOUNDER</span>
                </div>
                <h2 class="text-4xl font-heading text-white mb-2">{{ founder.name }}</h2>
                <h3 class="text-xl text-primary font-medium mb-8">{{ founder.role }}</h3>
                <div class="border-l-2 border-primary pl-6 mb-8">
                    <p class="text-gray-300 text-lg italic">"{{ founder.bio }}"</p>
                </div>
                <button class="border border-gray-600 text-white hover:bg-gray-800 px-6 py-2 rounded-sm text-sm font-bold uppercase tracking-wider transition">
                    View Profile
                </button>
            </div>
        </div>
        {% else %}
        <p class="text-gray-400">No founders found.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}'''


events_html = '''{% extends "base.html" %}
{% block title %}- Events{% endblock %}
{% block content %}
<!-- Hero -->
<div class="relative bg-background overflow-hidden border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-32">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8 items-center">
            <div>
                <h1 class="text-5xl md:text-7xl font-heading text-gray-500 uppercase tracking-tight mb-6 leading-none">
                    Meet.<br>Learn.<br>Connect.<br><span class="text-primary text-white">Build.</span>
                </h1>
                <p class="text-gray-400 text-lg mb-8 max-w-md">
                    Curated gatherings for Mumbai's ambitious founders, creators, and operators. From intimate workshops to high-impact founder conversations.
                </p>
                <a href="#upcoming" class="bg-primary hover:bg-primaryHover text-white px-8 py-3 rounded-md text-sm font-bold uppercase tracking-wider transition">
                    Explore Events
                </a>
            </div>
            <div class="mt-16 lg:mt-0 relative hidden lg:block">
                <!-- Abstract graphic representing cards -->
                <div class="relative w-full h-[400px]">
                    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-40 bg-surface border border-gray-700 rounded-lg shadow-2xl transform rotate-12 flex flex-col p-4 opacity-50"></div>
                    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-72 h-44 bg-surface border border-gray-600 rounded-lg shadow-2xl transform -rotate-6 flex flex-col p-6 z-10">
                        <span class="text-xs text-emerald-400 font-bold mb-2 uppercase">Workshop</span>
                        <h3 class="text-xl text-white font-heading">GTM Strategy</h3>
                        <p class="text-gray-400 text-xs mt-auto">24 Oct - BKC, Mumbai</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Events List -->
<div id="upcoming" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
    <p class="text-emerald-400 text-[10px] font-bold uppercase tracking-widest mb-4">Built in Mumbai</p>
    <h2 class="text-3xl font-heading text-gray-300 mb-12 uppercase">Upcoming Gatherings</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {% for event in events %}
        <div class="bg-surface border border-gray-800 rounded-lg overflow-hidden flex flex-col hover:border-gray-600 transition group">
            <div class="relative h-48 overflow-hidden">
                {% if event.image_filename %}
                <img src="{{ url_for('static', filename='uploads/events/' + event.image_filename) }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                {% else %}
                <div class="w-full h-full bg-gray-800"></div>
                {% endif %}
                <div class="absolute top-4 left-4 bg-primary/20 text-primary border border-primary text-[10px] font-bold px-2 py-0.5 rounded uppercase">UPCOMING</div>
            </div>
            <div class="p-6 flex flex-col flex-grow">
                <p class="text-[10px] text-emerald-400 font-bold mb-2 uppercase">{{ event.event_date.strftime('%b %d - %I:%M %p') }}</p>
                <h3 class="text-xl font-bold text-white mb-4 leading-tight">{{ event.title }}</h3>
                <div class="mt-auto pt-4 border-t border-gray-800">
                    <p class="text-gray-500 text-xs flex items-center">
                        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"></path></svg>
                        Mumbai
                    </p>
                </div>
            </div>
            <div class="px-6 pb-6">
                <button class="w-full border border-gray-600 text-white hover:bg-gray-800 py-2 rounded text-[10px] font-bold uppercase tracking-wider transition">
                    View Details
                </button>
            </div>
        </div>
        {% else %}
        <p class="text-gray-400 col-span-full">No upcoming events right now.</p>
        {% endfor %}
    </div>
    
    <div class="mt-16 text-center">
        <a href="#" class="text-[10px] text-gray-500 hover:text-white uppercase font-bold tracking-widest transition">VIEW ALL PAST EVENTS</a>
    </div>
</div>
{% endblock %}'''


blogs_html = '''{% extends "base.html" %}
{% block title %}- Blog{% endblock %}
{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    
    <!-- Featured Hero -->
    <div class="relative w-full h-[500px] rounded-xl overflow-hidden mb-20 group">
        <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=2000" class="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:scale-105 transition duration-700">
        <div class="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent"></div>
        <div class="absolute bottom-0 left-0 p-10 md:p-16 w-full md:w-2/3">
            <span class="text-primary text-[10px] font-bold uppercase tracking-widest mb-4 block">Ecosystem</span>
            <h1 class="text-4xl md:text-5xl font-heading text-white mb-6 leading-tight">The Architects of Mumbai's New Tech Stack</h1>
            <div class="flex items-center">
                <div class="w-10 h-10 rounded-full bg-gray-500 overflow-hidden mr-4 border-2 border-surface">
                    <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=100" class="w-full h-full object-cover">
                </div>
                <div>
                    <p class="text-white text-xs font-bold">Rahul Prasad</p>
                    <p class="text-gray-400 text-[10px] uppercase tracking-wider">Oct 12 - 5 min read</p>
                </div>
            </div>
        </div>
    </div>

    <h2 class="text-2xl font-heading text-white mb-8 border-b border-gray-800 pb-4">Latest Thinking</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {% for blog in blogs %}
        <div class="flex flex-col group cursor-pointer border-b border-gray-800 pb-6 md:border-none md:pb-0">
            <div class="relative h-56 overflow-hidden rounded-lg mb-6">
                {% if blog.image_filename %}
                <img src="{{ url_for('static', filename='uploads/blogs/' + blog.image_filename) }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                {% else %}
                <div class="w-full h-full bg-gray-800 flex items-center justify-center text-gray-600">No Image</div>
                {% endif %}
            </div>
            <div class="flex gap-2 mb-4">
                <span class="text-[9px] font-bold uppercase tracking-wider text-emerald-400 border border-emerald-400/30 px-2 py-0.5 rounded">STARTUPS</span>
                <span class="text-[9px] font-bold uppercase tracking-wider text-gray-400 border border-gray-700 px-2 py-0.5 rounded">{{ blog.created_at.strftime('%b %d') }}</span>
            </div>
            <h3 class="text-lg font-bold text-white mb-3 group-hover:text-primary transition leading-tight">{{ blog.title }}</h3>
            <p class="text-gray-400 text-xs mb-6 flex-grow line-clamp-3 leading-relaxed">{{ blog.content }}</p>
            <p class="text-[10px] text-gray-500 font-bold uppercase tracking-widest hover:text-white transition">READ ARTICLE +</p>
        </div>
        {% else %}
        <p class="text-gray-400">No blogs found.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}'''


mentors_html = '''{% extends "base.html" %}
{% block title %}- Mentorship{% endblock %}
{% block content %}
<!-- Hero -->
<div class="relative bg-background overflow-hidden border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-32">
        <div class="lg:grid lg:grid-cols-2 lg:gap-16 items-center">
            <div>
                <h1 class="text-5xl md:text-7xl font-heading text-white uppercase tracking-tight mb-6 leading-none">
                    YOU DON'T HAVE<br>TO FIGURE IT OUT<br><span class="text-primary">ALONE.</span>
                </h1>
                <p class="text-gray-400 text-base mb-10 max-w-lg leading-relaxed">
                    Connect with people who have already walked parts of the path you're trying to build. A community designed for Mumbai's most ambitious founders.
                </p>
                <button class="bg-primary hover:bg-primaryHover text-white px-8 py-3 rounded text-[10px] font-bold uppercase tracking-wider transition">
                    FIND A MENTOR >
                </button>
            </div>
            <div class="mt-16 lg:mt-0 hidden lg:block">
                <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=800" class="rounded-xl grayscale opacity-60">
            </div>
        </div>
    </div>
</div>

<!-- Value Props -->
<div class="bg-[#0f1115] py-24 border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-2xl md:text-3xl font-heading text-gray-300 mb-16 max-w-xl uppercase tracking-wider">
            THE RIGHT CONVERSATION CAN CHANGE YOUR DIRECTION.
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div class="border-t border-gray-800 pt-6">
                <p class="text-5xl font-heading text-primary mb-4 opacity-80">01</p>
                <h3 class="text-lg font-bold text-white mb-3">Clarity</h3>
                <p class="text-gray-400 text-xs leading-relaxed">Cut through the noise. Get actionable insights on product strategy and go-to-market from those who have successfully navigated the early stages.</p>
            </div>
            <div class="border-t border-gray-800 pt-6">
                <p class="text-5xl font-heading text-primary mb-4 opacity-80">02</p>
                <h3 class="text-lg font-bold text-white mb-3">Direction</h3>
                <p class="text-gray-400 text-xs leading-relaxed">Avoid common pitfalls. A mentor acts as a sounding board, helping you refine your roadmap and prioritize what actually moves the needle.</p>
            </div>
            <div class="border-t border-gray-800 pt-6">
                <p class="text-5xl font-heading text-primary mb-4 opacity-80">03</p>
                <h3 class="text-lg font-bold text-white mb-3">Confidence</h3>
                <p class="text-gray-400 text-xs leading-relaxed">Building is lonely. Having someone in your corner who understands the pressure provides the resilience needed to keep going.</p>
            </div>
        </div>
    </div>
</div>

<!-- Mentors Grid -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
    <h2 class="text-2xl font-heading text-white mb-12 uppercase">Meet Our Mentors</h2>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        {% for mentor in mentors %}
        <div class="bg-surface border border-gray-800 rounded p-6 text-center hover:border-gray-600 transition flex flex-col items-center">
            {% if mentor.image_filename %}
            <img src="{{ url_for('static', filename='uploads/mentors/' + mentor.image_filename) }}" class="w-20 h-20 rounded-full mb-4 object-cover grayscale">
            {% else %}
            <div class="w-20 h-20 rounded-full mb-4 bg-gray-800 flex items-center justify-center text-gray-500">Img</div>
            {% endif %}
            <h5 class="text-sm font-bold text-white mb-1">{{ mentor.name }}</h5>
            <h6 class="text-[10px] text-primary font-bold uppercase tracking-wider mb-4">{{ mentor.expertise }}</h6>
            <p class="text-xs text-gray-500 line-clamp-3 leading-relaxed">{{ mentor.bio }}</p>
        </div>
        {% else %}
        <p class="text-gray-400 col-span-full">No mentors found.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}'''


community_html = '''{% extends "base.html" %}
{% block title %}- Community{% endblock %}
{% block content %}
<!-- Hero -->
<div class="relative overflow-hidden py-20 border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-12 items-center">
            <div>
                <h1 class="text-5xl md:text-6xl font-heading text-white uppercase tracking-tight mb-6 leading-none">
                    MEET THE PEOPLE<br>BUILDING WHAT'S<br><span class="text-primary">NEXT.</span>
                </h1>
                <p class="text-gray-400 text-sm mb-8 max-w-sm leading-relaxed">
                    Join Mumbai's most ambitious network of founders, creators, and builders. A diverse ecosystem united by a singular drive to create.
                </p>
                <a href="{{ url_for('public_signup') }}" class="bg-primary hover:bg-primaryHover text-white px-6 py-2 rounded text-[10px] font-bold uppercase tracking-wider transition inline-block">
                    JOIN THE NETWORK +
                </a>
            </div>
            <div class="mt-12 lg:mt-0">
                <img src="https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&q=80&w=800" class="rounded object-cover h-[350px] w-full grayscale opacity-80 border border-gray-700">
            </div>
        </div>
    </div>
</div>

<!-- Grid section -->
<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
    <div class="flex justify-between items-center mb-10 pb-4">
        <div>
            <h2 class="text-xl font-heading text-white mb-4 uppercase tracking-wider">FIND YOUR PEOPLE.</h2>
            <div class="flex space-x-2">
                <span class="px-3 py-1 bg-primary text-white text-[9px] font-bold rounded uppercase tracking-wider cursor-pointer">ALL</span>
                <span class="px-3 py-1 bg-surface border border-gray-700 text-gray-400 text-[9px] font-bold rounded uppercase tracking-wider cursor-pointer hover:bg-gray-800 transition">FOUNDERS</span>
                <span class="px-3 py-1 bg-surface border border-gray-700 text-gray-400 text-[9px] font-bold rounded uppercase tracking-wider cursor-pointer hover:bg-gray-800 transition">CREATORS</span>
            </div>
        </div>
        <div class="hidden md:block">
            <div class="relative">
                <input type="text" placeholder="Search members..." class="bg-surface border border-gray-800 rounded py-1.5 px-3 text-xs text-white focus:outline-none focus:border-gray-600">
                <svg class="absolute right-2 top-2 w-3 h-3 text-gray-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path></svg>
            </div>
        </div>
    </div>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- Mock Member Cards as per design -->
        <div class="bg-surface border border-gray-800 rounded p-3 hover:border-gray-600 transition flex flex-col">
            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150" class="w-full aspect-square object-cover rounded-sm mb-3 grayscale">
            <h4 class="text-white font-bold text-xs mb-0.5">Karan Desai</h4>
            <p class="text-gray-500 text-[10px] mb-3">Founder, FinTech</p>
            <div class="flex gap-1 mt-auto flex-wrap">
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">FINTECH</span>
            </div>
            <div class="mt-3 text-[9px] text-primary font-bold uppercase tracking-wider hover:text-white cursor-pointer transition">View Profile +</div>
        </div>
        <div class="bg-surface border border-gray-800 rounded p-3 hover:border-gray-600 transition flex flex-col">
            <img src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=150" class="w-full aspect-square object-cover rounded-sm mb-3 grayscale">
            <h4 class="text-white font-bold text-xs mb-0.5">Priya Sharma</h4>
            <p class="text-gray-500 text-[10px] mb-3">Creative Director</p>
            <div class="flex gap-1 mt-auto flex-wrap">
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">DESIGN</span>
            </div>
            <div class="mt-3 text-[9px] text-primary font-bold uppercase tracking-wider hover:text-white cursor-pointer transition">View Profile +</div>
        </div>
        <div class="bg-surface border border-gray-800 rounded p-3 hover:border-gray-600 transition flex flex-col">
            <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150" class="w-full aspect-square object-cover rounded-sm mb-3 grayscale">
            <h4 class="text-white font-bold text-xs mb-0.5">Rohan Mehta</h4>
            <p class="text-gray-500 text-[10px] mb-3 leading-tight">Managing Partner, Elevate</p>
            <div class="flex gap-1 mt-auto flex-wrap">
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">INVESTMENT</span>
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">STRATEGY</span>
            </div>
            <div class="mt-3 text-[9px] text-primary font-bold uppercase tracking-wider hover:text-white cursor-pointer transition">View Profile +</div>
        </div>
        <div class="bg-surface border border-gray-800 rounded p-3 hover:border-gray-600 transition flex flex-col">
            <img src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=150" class="w-full aspect-square object-cover rounded-sm mb-3 grayscale">
            <h4 class="text-white font-bold text-xs mb-0.5">Ananya Iyer</h4>
            <p class="text-gray-500 text-[10px] mb-3 leading-tight">Head of Product, NuApp</p>
            <div class="flex gap-1 mt-auto flex-wrap">
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">PRODUCT</span>
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">SAAS</span>
            </div>
            <div class="mt-3 text-[9px] text-primary font-bold uppercase tracking-wider hover:text-white cursor-pointer transition">View Profile +</div>
        </div>
        <div class="bg-surface border border-gray-800 rounded p-3 hover:border-gray-600 transition flex flex-col">
            <img src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=150" class="w-full aspect-square object-cover rounded-sm mb-3 grayscale">
            <h4 class="text-white font-bold text-xs mb-0.5">Vikram Singh</h4>
            <p class="text-gray-500 text-[10px] mb-3">Founder, TechWave</p>
            <div class="flex gap-1 mt-auto flex-wrap">
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">HARDWARE</span>
            </div>
            <div class="mt-3 text-[9px] text-primary font-bold uppercase tracking-wider hover:text-white cursor-pointer transition">View Profile +</div>
        </div>
        <div class="bg-surface border border-gray-800 rounded p-3 hover:border-gray-600 transition flex flex-col">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150" class="w-full aspect-square object-cover rounded-sm mb-3 grayscale">
            <h4 class="text-white font-bold text-xs mb-0.5">Meera Kapoor</h4>
            <p class="text-gray-500 text-[10px] mb-3 leading-tight">Lead Designer, UI/UX Studio</p>
            <div class="flex gap-1 mt-auto flex-wrap">
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">DESIGN</span>
                <span class="text-[8px] bg-gray-900 border border-gray-800 px-1 py-0.5 rounded text-gray-400 font-bold uppercase tracking-wider">AGENCY</span>
            </div>
            <div class="mt-3 text-[9px] text-primary font-bold uppercase tracking-wider hover:text-white cursor-pointer transition">View Profile +</div>
        </div>
    </div>
</div>
{% endblock %}'''

with open(os.path.join(base_dir, "founders.html"), "w", encoding="utf-8") as f:
    f.write(founders_html)
with open(os.path.join(base_dir, "events.html"), "w", encoding="utf-8") as f:
    f.write(events_html)
with open(os.path.join(base_dir, "blogs.html"), "w", encoding="utf-8") as f:
    f.write(blogs_html)
with open(os.path.join(base_dir, "mentors.html"), "w", encoding="utf-8") as f:
    f.write(mentors_html)
with open(os.path.join(base_dir, "community.html"), "w", encoding="utf-8") as f:
    f.write(community_html)
