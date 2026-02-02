import 'package:client/data/constants/app_typography.dart';
import 'package:client/modules/widgets/buttons/primary_button.dart';
import 'package:flutter/material.dart';

class ListEmptyCard extends StatelessWidget {
  final String icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;
  const ListEmptyCard({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Image.asset(icon),
        SizedBox(height: 31),
        Text(title, style: AppTypography.kBold20),
        Text(
          subtitle,
          style: AppTypography.kLight14,
          textAlign: TextAlign.center,
        ),
        SizedBox(height: 20),
        PrimaryButton(onTap: () {}, text: 'View All Services', width: 166),
      ],
    );
  }
}
