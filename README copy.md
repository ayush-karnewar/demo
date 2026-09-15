# 🍕 FoodHub - Food Delivery App

A beautiful, modern food delivery application inspired by Domino's with a stunning blue theme, smooth animations, and complete authentication system.

## ✨ Features

- **Home Page**: 
  - Hero section with automatic slideshow (3 rotating images)
  - Special offers section with promotional codes
  - Top bestselling items showcase
  
- **Menu Page**:
  - 10 diverse food items with custom SVG illustrations
  - Category filtering (Pizza, Burgers, Chicken, Drinks)
  - Real-time search functionality
  - Beautiful card-based layout with hover animations

- **Authentication**:
  - User registration and login system
  - Secure password validation
  - User session management with localStorage
  - Logout functionality

- **Shopping Cart**:
  - Fixed sidebar cart with live updates
  - Add/remove items functionality
  - Real-time total calculation
  - Persistent cart storage

- **UI/UX**:
  - Modern blue color scheme (Domino's inspired)
  - Responsive design (works on all devices)
  - Smooth animations and transitions
  - Intuitive navigation
  - Beautiful notifications

## 📁 Project Structure

```
Food App/
├── index.html          # Home page
├── menu.html           # Menu page with all items
├── style.css           # Global styles and animations
├── script.js           # Core JavaScript functionality
├── .env                # Environment configuration (Supabase keys)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🚀 Getting Started

### 1. Clone/Download the Project
```bash
# Download the folder or clone from repository
cd "Food App"
```

### 2. Set Up Supabase (Optional but Recommended)

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Project Settings → API
4. Copy your `Project URL` and `anon public key`
5. Update `.env` file:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   ```

### 3. Run the App

**Option A: Using Python**
```bash
python -m http.server 8000
# Visit http://localhost:8000
```

**Option B: Using Node.js**
```bash
npx http-server
# Visit http://localhost:8080
```

**Option C: Using Live Server (VS Code)**
- Install "Live Server" extension
- Right-click index.html → "Open with Live Server"

## 📖 How to Use

### Navigation
- **Home**: View featured items and offers
- **Menu**: Browse all 10 food items with filters
- **Login**: Create account or sign in

### Shopping
1. Browse items on Menu page
2. Click "Add to Cart" on any item
3. View your cart on the right sidebar
4. Click "Checkout" to complete order
5. Must be logged in to checkout

### Searching
- Use the search bar on Menu page to find items
- Filter by category: All, Pizza, Burgers, Chicken, Drinks

### Offers
- Copy promo codes from the Offers section
- Apply them during checkout (simulated)

## 🎨 Customization

### Change Colors
Edit `:root` variables in `style.css`:
```css
:root {
    --primary-blue: #0055cc;      /* Main blue */
    --dark-blue: #003d99;         /* Darker blue */
    --accent-red: #ff5722;        /* Red accent */
    /* ... more variables ... */
}
```

### Add More Food Items
1. Open `menu.html`
2. Copy a `.menu-card` div
3. Update the SVG, title, description, price
4. Add `data-category="category_name"` attribute

### Modify Hero Slideshow
1. Edit the slides in `index.html` (`.slide` divs)
2. Change image URLs or add new slides
3. Add corresponding dots

## 🔐 Authentication Notes

**Current Implementation**: 
- Uses localStorage for session management (demo)
- Passwords validated on frontend (min 6 characters)
- Email format validation

**Production Setup with Supabase**:
```javascript
// Install Supabase client
npm install @supabase/supabase-js

// Use Supabase in script.js
import { createClient } from '@supabase/supabase-js'
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
```

## 📱 Responsive Design

App works perfectly on:
- 📱 Mobile phones (320px and up)
- 📱 Tablets (768px and up)
- 🖥️ Desktop screens (1024px and up)

## 🐛 Bug Fixes Included

- ✅ Form submission without page reload
- ✅ Cart persists across page refresh
- ✅ Modal closes when clicking outside
- ✅ Slider auto-rotates smoothly
- ✅ Search works across all items
- ✅ Responsive image scaling
- ✅ Loading states for auth
- ✅ Input validation and error messages
- ✅ Notification animations

## 📦 Dependencies

This is a **zero-dependency** project!
- Pure HTML5
- Vanilla CSS3 (with animations)
- Vanilla JavaScript (ES6+)
- No external frameworks needed

## 🎯 Future Enhancements

- [ ] Real Supabase integration
- [ ] Payment gateway (Stripe/PayPal)
- [ ] Order tracking
- [ ] User profile and order history
- [ ] Admin dashboard
- [ ] Real database for items
- [ ] Image upload for items
- [ ] Rating and review system
- [ ] Push notifications
- [ ] Mobile app version

## 📄 License

Free to use and modify. Enjoy! 🎉

## 🤝 Support

For issues or improvements, feel free to modify and customize the code.

---

**Made with ❤️ for food delivery enthusiasts**
