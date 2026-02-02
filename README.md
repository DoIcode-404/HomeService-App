# HomeService App

A comprehensive Flutter-based home service booking application that connects users with various home service providers.

## Features

- **Multiple Service Categories**: Cleaning, Plumbing, Electrical, Appliance Repair, Painting, Shifting, Beauty Services, and more
- **User Authentication**: Sign up/Sign in with phone verification
- **Booking Management**: Schedule, track, and manage service bookings
- **Calendar Integration**: View and manage appointments
- **Payment Methods**: Multiple payment options support
- **Real-time Notifications**: Stay updated on booking status
- **Offers & Rewards**: Promotional codes and reward points system
- **Live Chat Support**: Customer support with chat functionality
- **Multi-platform**: Supports Android, iOS, Web, Windows, Linux, and macOS

## Getting Started

### Prerequisites

- Flutter SDK (latest stable version)
- Dart SDK
- Android Studio / Xcode (for mobile development)
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/DoIcode-404/HomeService-App.git
cd HomeService-App
```

2. Navigate to the client directory:

```bash
cd client
```

3. Install dependencies:

```bash
flutter pub get
```

4. Run the app:

```bash
flutter run
```

## Project Structure

```
client/
├── lib/
│   ├── bindings/          # Dependency injection bindings
│   ├── controllers/       # GetX controllers
│   ├── data/             # Constants and helpers
│   ├── model/            # Data models
│   ├── modules/          # UI screens and widgets
│   ├── routes/           # App routing
│   └── services/         # App services
├── assets/               # Images, icons, and other assets
└── android/ios/web/      # Platform-specific code
```

## Technologies Used

- **Flutter** - UI framework
- **GetX** - State management and routing
- **Dart** - Programming language

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
