import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/animations/button_animation.dart';

import 'package:flutter/material.dart';

class NextButton extends StatelessWidget {
  final VoidCallback onTap;
  const NextButton({required this.onTap, super.key});

  @override
  Widget build(BuildContext context) {
    return ButtonAnimation(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.all(12),
        decoration: const BoxDecoration(
          color: AppColors.kPrimary,
          shape: BoxShape.circle,
        ),
        child: Icon(Icons.navigate_next, size: 30, color: AppColors.kWhite),
      ),
    );
  }
}
