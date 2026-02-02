import 'package:client/data/constants/constants.dart';
import 'package:client/model/onboarding.dart';
import 'package:client/modules/auth/sign_in.dart';
import 'package:client/modules/onboarding/components/next_button.dart';
import 'package:client/modules/onboarding/components/onboarding_card.dart';
import 'package:client/modules/onboarding/components/skip_button.dart';
import 'package:client/modules/widgets/buttons/primary_button.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  OnboardingScreenState createState() => OnboardingScreenState();
}

class OnboardingScreenState extends State<OnboardingScreen> {
  int _currentPageIndex = 0;
  final _pageController = PageController();

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;
    return Scaffold(
      backgroundColor:
          isDarkMode(context) ? AppColors.kDarkBackground : AppColors.kWhite,
      appBar: AppBar(
        backgroundColor:
            isDarkMode(context) ? AppColors.kDarkBackground : AppColors.kWhite,
        actions: [
          SkipButton(
            onTap: () {
              Get.offAll(() => const SignIn());
            },
          ),
          SizedBox(width: 16),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: PageView.builder(
              itemCount: onboardingList.length,
              controller: _pageController,
              physics: const NeverScrollableScrollPhysics(),
              onPageChanged: (index) {
                setState(() {
                  _currentPageIndex = index;
                });
              },
              itemBuilder: (context, index) {
                return OnboardingCard(
                  playAnimation: true,
                  onboarding: onboardingList[index],
                );
              },
            ),
          ),
          SmoothPageIndicator(
            controller: _pageController,
            count: onboardingList.length,
            effect: WormEffect(
              dotHeight: 8,
              dotWidth: 8,
              dotColor: AppColors.kPrimary.withOpacity(0.2),
            ),
            onDotClicked: (index) {
              setState(() {
                _currentPageIndex = index;
              });
              _pageController.animateToPage(
                index,
                duration: const Duration(milliseconds: 500),
                curve: Curves.easeInOut,
              );
            },
          ),
          SizedBox(height: 30),
          (_currentPageIndex < onboardingList.length - 1)
              ? NextButton(
                onTap: () {
                  _pageController.nextPage(
                    duration: const Duration(milliseconds: 500),
                    curve: Curves.easeInOut,
                  );
                },
              )
              : PrimaryButton(
                onTap: () {
                  Get.offAll(() => const SignIn(), transition: Transition.zoom);
                },
                width: 166,
                text: 'Get Started',
              ),
          SizedBox(height: 20),
        ],
      ),
    );
  }
}
