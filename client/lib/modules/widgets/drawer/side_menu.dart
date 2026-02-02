import 'package:client/data/constants/constants.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class SideMenu extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final String icon;
  final bool isSelected;
  const SideMenu({
    super.key,
    this.isSelected = false,
    this.onPressed,
    required this.text,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        AnimatedPositioned(
          duration: const Duration(milliseconds: 300),
          curve: Curves.fastOutSlowIn,
          width: isSelected ? 240 : 0,
          height: 50,
          left: 0,
          child: Container(
            width: 10,
            decoration: BoxDecoration(
              color: AppColors.kWhite,
              borderRadius: BorderRadius.circular(10),
            ),
          ),
        ),
        ListTile(
          onTap: onPressed,
          contentPadding: EdgeInsets.symmetric(horizontal: 12),
          dense: true,
          minLeadingWidth: 10,
          leading: SizedBox(
            width: 28,
            height: 28,
            child: SvgPicture.asset(
              icon,
              colorFilter: ColorFilter.mode(
                isSelected ? AppColors.kPrimary : AppColors.kWhite,
                BlendMode.srcIn,
              ),
            ),
          ),
          title: Text(
            text,
            style: AppTypography.kMedium15.copyWith(
              color: isSelected ? AppColors.kPrimary : AppColors.kWhite,
            ),
          ),
        ),
      ],
    );
  }
}
