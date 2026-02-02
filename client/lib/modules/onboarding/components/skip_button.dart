import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/animations/button_animation.dart';
import 'package:flutter/material.dart';

class SkipButton extends StatelessWidget {
  final VoidCallback onTap;
  const SkipButton({required this.onTap, super.key});

  @override
  Widget build(BuildContext context) {
    return ButtonAnimation(
      onTap: onTap,
      child: Center(
        child: Container(
          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(30),
            color: AppColors.kAccent4,
          ),
          child: Text(
            'Skip',
            style: AppTypography.kLight14.copyWith(color: Colors.black),
          ),
        ),
      ),
    );
  }
}
