import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class ServiceProviderCard extends StatelessWidget {
  const ServiceProviderCard({super.key});

  @override
  Widget build(BuildContext context) {
    return PrimaryContainer(
      child: Column(
        children: [
          Row(
            children: [
              CustomHeaderText(text: 'Services Provider', fontSize: 18),
              const Spacer(),
              CustomButton(
                isBorder: true,
                text: 'Timeline',
                icon: AppAssets.kArrowForward,
                onTap: () {},
              ),
            ],
          ),
          SizedBox(height: 16),
          Row(
            children: [
              Container(
                height: 55,
                width: 55,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: AppColors.kInput),
                ),
                child: Image.asset(AppAssets.kServiceProvider),
              ),
              SizedBox(width: 16),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Westinghouse', style: AppTypography.kMedium16),
                  SizedBox(height: 5),
                  Text(
                    'Air Conditioning',
                    style: AppTypography.kLight14.copyWith(
                      color: AppColors.kNeutral,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}
