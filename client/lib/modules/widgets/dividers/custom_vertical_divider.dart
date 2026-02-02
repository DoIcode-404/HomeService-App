import 'package:client/data/constants/constants.dart';
import 'package:flutter/material.dart';

class CustomVerticalDivider extends StatelessWidget {
  final double? height;
  final double? width;
  final Color? color;
  const CustomVerticalDivider({super.key, this.height, this.width, this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height ?? 20,
      width: width ?? 2,
      decoration: BoxDecoration(
        color: color ?? AppColors.kPrimary,
        borderRadius: BorderRadius.circular(AppSpacing.radiusForty),
      ),
    );
  }
}
