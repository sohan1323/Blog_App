# Django Blog WebApp - System Architecture Document

## 1. Project Overview

A multi-user blog platform built with Django that supports content creation, user management, and social interactions through likes/dislikes.

---

## 2. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  - Templates (HTML/CSS/JS)                                       │
│  - Django Forms (User/Profile/Post Management)                   │
│  - Static Files (CSS, JS, Images)                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  Views Layer:                                                    │
│    - Class-Based Views (CBVs) / Function-Based Views (FBVs)     │
│    - Authentication Views (Login, Logout, Register)              │
│    - Profile Views (CRUD)                                        │
│    - Post Views (CRUD + Like/Dislike)                           │
│                                                                  │
│  Business Logic:                                                 │
│    - Permission Mixins (User/Superuser)                         │
│    - Custom Validators                                           │
│    - Signal Handlers (Auto Profile Creation, etc.)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Models:                                                         │
│    - User (Extended Django User)                                 │
│    - Profile                                                     │
│    - Post                                                        │
│    - PostImage                                                   │
│    - PostFile                                                    │
│    - PostLike                                                    │
│                                                                  │
│  Django ORM ← → Database (PostgreSQL/MySQL/SQLite)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  - Media Storage (User Uploads)                                  │
│  - Static Files Storage                                          │
│  - Database                                                      │
│  - Cache (Optional: Redis)                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Database Schema Design

### 3.1 User Model (Extended Django Auth User)
```python
# Using Django's built-in User model with email authentication
User (Django's default)
├── id (PK, Auto)
├── username (Unique)
├── email (Unique, Required)
├── password (Hashed)
├── is_active (Boolean)
├── is_staff (Boolean)  # Superuser flag
├── is_superuser (Boolean)
├── date_joined (DateTime)
└── last_login (DateTime)
```

### 3.2 Profile Model
```python
Profile
├── id (PK, Auto)
├── user (FK → User, OneToOne)
├── profile_image (ImageField, Optional)
├── name (CharField, Max 100)
├── bio/description (TextField, Optional)
├── created_at (DateTime, Auto)
└── updated_at (DateTime, Auto)
```

### 3.3 Post Model
```python
Post
├── id (PK, Auto)
├── author (FK → User)
├── title (CharField, Max 200)
├── content (TextField)
├── slug (SlugField, Unique)
├── status (CharField: Draft/Published)
├── created_at (DateTime, Auto)
├── updated_at (DateTime, Auto)
└── published_at (DateTime, Nullable)
```

### 3.4 PostImage Model (Multiple Images per Post)
```python
PostImage
├── id (PK, Auto)
├── post (FK → Post)
├── image (ImageField)
├── caption (CharField, Optional)
├── order (IntegerField, Default 0)
└── uploaded_at (DateTime, Auto)
```

### 3.5 PostFile Model (Attachments)
```python
PostFile
├── id (PK, Auto)
├── post (FK → Post)
├── file (FileField)
├── file_name (CharField)
├── file_size (IntegerField)
└── uploaded_at (DateTime, Auto)
```

### 3.6 PostLike Model (Likes/Dislikes)
```python
PostLike
├── id (PK, Auto)
├── user (FK → User)
├── post (FK → Post)
├── is_like (Boolean: True=Like, False=Dislike)
├── created_at (DateTime, Auto)
└── UNIQUE_TOGETHER: (user, post)
```

---

## 4. User Roles & Permissions

### 4.1 Normal User Permissions
| Feature | Create | Read | Update | Delete |
|---------|--------|------|--------|--------|
| Own Profile | ✓ | ✓ | ✓ | ✓ |
| Other Profiles | ✗ | ✓ | ✗ | ✗ |
| Own Posts | ✓ | ✓ | ✓ | ✓ |
| Other Posts | ✗ | ✓ | ✗ | ✗ |
| Like/Dislike Posts | ✓ | ✓ | ✓ (own) | ✓ (own) |

### 4.2 Superuser Permissions
| Feature | Create | Read | Update | Delete |
|---------|--------|------|--------|--------|
| Own Profile | ✓ | ✓ | ✓ | ✓ |
| Other Profiles | ✗ | ✓ | ✗ | ✓ |
| Own Posts | ✓ | ✓ | ✓ | ✓ |
| Other Posts | ✗ | ✓ | ✗ | ✓ |
| Like/Dislike Posts | ✓ | ✓ | ✓ | ✓ |

**Note:** Superusers can delete normal user profiles and their posts but cannot update them (maintains data integrity).

---

## 5. Django Apps Structure

```
blog_project/
├── config/                      # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/               # User authentication & profiles
│   │   ├── models.py          # Profile model
│   │   ├── views.py           # Auth views, profile CRUD
│   │   ├── forms.py           # Registration, profile forms
│   │   ├── signals.py         # Auto-create profile on user creation
│   │   └── urls.py
│   │
│   ├── posts/                  # Blog posts
│   │   ├── models.py          # Post, PostImage, PostFile models
│   │   ├── views.py           # Post CRUD views
│   │   ├── forms.py           # Post creation/edit forms
│   │   └── urls.py
│   │
│   └── interactions/           # Likes/Dislikes
│       ├── models.py          # PostLike model
│       ├── views.py           # Like/dislike toggle
│       └── urls.py
│
├── templates/
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── posts/
│       ├── post_list.html
│       ├── post_detail.html
│       └── post_form.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                      # User uploads
│   ├── profiles/
│   ├── posts/
│   └── files/
│
└── manage.py
```

---

## 6. Authentication System

### 6.1 Authentication Backend
```python
# Email + Password authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default (username/email)
]

# Custom user authentication
# Option 1: Use email as username
# Option 2: Add custom backend for email auth
```

### 6.2 Key Features
- **Registration:** Email + Password (with email verification optional)
- **Login:** Email or Username + Password
- **Password Reset:** Email-based password recovery
- **Session Management:** Django sessions
- **Password Validation:** Django's built-in validators

### 6.3 Security Measures
- CSRF protection (Django default)
- Password hashing (PBKDF2/Argon2)
- Login throttling (django-axes recommended)
- Secure password requirements
- Email verification (optional but recommended)

---

## 7. URL Structure

```
# Authentication URLs
/accounts/login/              → Login page
/accounts/register/           → User registration
/accounts/logout/             → Logout
/accounts/password-reset/     → Password reset

# Profile URLs
/profile/<username>/          → View profile
/profile/edit/                → Edit own profile
/profile/delete/              → Delete own profile
/profiles/                    → List all profiles (optional)

# Post URLs
/                            → Home/Post list (all published posts)
/posts/create/               → Create new post
/posts/<slug>/               → Post detail view
/posts/<slug>/edit/          → Edit post (author only)
/posts/<slug>/delete/        → Delete post (author/superuser)
/posts/my-posts/             → User's own posts
/posts/<slug>/like/          → Toggle like
/posts/<slug>/dislike/       → Toggle dislike

# Admin URLs
/admin/                      → Django admin (superuser only)
```

---

## 8. Key Features Implementation

### 8.1 Profile Management
```python
# Auto-create profile on user registration (using signals)
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

### 8.2 Post Creation with Multiple Files
```python
# Using Django Formsets for multiple images/files
from django.forms import inlineformset_factory

PostImageFormSet = inlineformset_factory(
    Post, PostImage, 
    fields=['image', 'caption'], 
    extra=3, 
    can_delete=True
)
```

### 8.3 Like/Dislike System
```python
# Toggle like/dislike
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = PostLike.objects.get_or_create(
        user=request.user, 
        post=post,
        defaults={'is_like': True}
    )
    if not created:
        if like.is_like:
            like.delete()  # Remove like
        else:
            like.is_like = True  # Change dislike to like
            like.save()
```

### 8.4 Permission Mixins
```python
# Custom mixin for post ownership
from django.contrib.auth.mixins import UserPassesTestMixin

class PostOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
```

---

## 9. Views Architecture

### 9.1 Class-Based Views (Recommended)
```python
# Example: Post CRUD
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-created_at')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PostOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

class PostDeleteView(LoginRequiredMixin, PostOwnerMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')
```

---

## 10. Additional Recommendations

### 10.1 Essential Django Packages
```python
# requirements.txt
Django>=4.2
Pillow                    # Image handling
django-crispy-forms       # Better forms
django-cleanup            # Auto-delete old files
django-filter             # Advanced filtering
django-taggit             # Tags for posts (optional)
```

### 10.2 Security Best Practices
- Set `DEBUG = False` in production
- Use environment variables for secrets
- Implement HTTPS
- Add rate limiting for login attempts
- Regular security updates

### 10.3 Performance Optimizations
- Use `select_related()` and `prefetch_related()` for queries
- Implement caching (Redis) for frequently accessed data
- Optimize image uploads (compression, thumbnails)
- Database indexing on frequently queried fields

### 10.4 Testing Strategy
- Unit tests for models
- Integration tests for views
- Permission tests for user roles
- Form validation tests

### 10.5 Future Enhancements
- **Comments System:** Add comments on posts
- **Tags/Categories:** Organize posts by topics
- **Search Functionality:** Full-text search
- **Notifications:** Email/in-app notifications
- **Social Sharing:** Share posts on social media
- **Draft System:** Save posts as drafts
- **Rich Text Editor:** CKEditor/TinyMCE for post content
- **User Following:** Follow other users
- **Post Analytics:** View counts, engagement metrics
- **API:** Django REST Framework for mobile apps

---

## 11. Development Workflow

### Phase 1: Foundation (Week 1-2)
1. Set up Django project structure
2. Configure database and authentication
3. Create User and Profile models
4. Implement registration/login system

### Phase 2: Core Features (Week 3-4)
1. Build Post model with CRUD operations
2. Implement file/image upload system
3. Add permission system
4. Create basic templates

### Phase 3: Interactions (Week 5)
1. Implement like/dislike system
2. Add profile management features
3. Superuser delete functionality

### Phase 4: Polish (Week 6)
1. UI/UX improvements
2. Testing and bug fixes
3. Performance optimization
4. Documentation

---

## 12. Deployment Considerations

### 12.1 Production Checklist
- [ ] Set up production database (PostgreSQL recommended)
- [ ] Configure static files serving (WhiteNoise/CDN)
- [ ] Set up media files storage (AWS S3/Cloud Storage)
- [ ] Configure email backend (SendGrid/Mailgun)
- [ ] Set up monitoring and logging
- [ ] Configure HTTPS/SSL
- [ ] Set up backup system

### 12.2 Hosting Options
- **PaaS:** Heroku, Railway, Render
- **VPS:** DigitalOcean, AWS EC2, Linode
- **Serverless:** AWS Lambda with Zappa

---

## 13. Database Relationships Diagram

```
User (1) ──────────── (1) Profile
  │
  │ (1)
  │
  ├─────── (Many) Post
  │                  │
  │                  │ (1)
  │                  │
  │                  ├─── (Many) PostImage
  │                  │
  │                  ├─── (Many) PostFile
  │                  │
  │                  └─── (Many) PostLike
  │                              │
  └──────────────────────────────┘
        (Many)          (1)
```

---

## 14. Sample Settings Configuration

```python
# settings.py key configurations

# Authentication
AUTH_USER_MODEL = 'auth.User'  # Using default User model
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Email authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Email configuration (development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Security
CSRF_COOKIE_SECURE = True  # Production
SESSION_COOKIE_SECURE = True  # Production
SECURE_SSL_REDIRECT = True  # Production
```

---

## 15. Testing Examples

```python
# tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_creation(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        self.assertEqual(post.author, self.user)
        self.assertEqual(str(post), 'Test Post')
```

---

## End of Document

This architecture provides a solid foundation for your Django blog webapp. You can use this as a reference during development or pass it to an agent for implementation guidance.
