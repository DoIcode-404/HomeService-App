import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/buttons/primary_button.dart';
import 'package:flutter/material.dart';

class CustomShowCaseWidget extends StatelessWidget {
  final String title;
  final String description;
  final String widgetNumber;
  final VoidCallback onNextTap;
  final String buttonText;
  const CustomShowCaseWidget({
    super.key,
    required this.title,
    required this.buttonText,
    required this.description,
    required this.widgetNumber,
    required this.onNextTap,
  });

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return Container(
      width: 300,
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.kPrimary,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: AppTypography.kMedium16.copyWith(color: AppColors.kWhite),
          ),
          SizedBox(height: 2),
          Text(
            description,
            style: AppTypography.kExtraLight13.copyWith(
              color: AppColors.kWhite,
            ),
          ),
          SizedBox(height: 30),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '$widgetNumber of 2',
                style: AppTypography.kLight12.copyWith(color: AppColors.kWhite),
              ),
              PrimaryButton(
                onTap: onNextTap,
                text: buttonText,
                fontSize: 12,
                height: 30,
                width: 60,
                borderRadius: 30,
                color:
                    isDarkMode(context)
                        ? AppColors.kSecondary
                        : AppColors.kWhite,
              ),
            ],
          ),
        ],
      ),
    );
  }
}
