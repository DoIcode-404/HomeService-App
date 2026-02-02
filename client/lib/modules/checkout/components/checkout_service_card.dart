import 'package:client/data/constants/constants.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class CheckoutServiceCard extends StatelessWidget {
  const CheckoutServiceCard({super.key});

  @override
  Widget build(BuildContext context) {
    return PrimaryContainer(
      child: Column(
        children: [
          Row(
            children: [
              CustomHeaderText(text: 'Service', fontSize: 18),
              const Spacer(),
              const Icon(Icons.more_horiz),
            ],
          ),
          SizedBox(height: 16),
          Row(
            children: [
              Container(
                height: 55,
                width: 55,
                padding: EdgeInsets.all(17),
                decoration: const BoxDecoration(
                  shape: BoxShape.circle,
                  color: AppColors.kAccent1,
                ),
                child: SvgPicture.asset(AppAssets.kAcRepair),
              ),
              SizedBox(width: 16),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'AC Installation (Both Unit)',
                    style: AppTypography.kMedium16,
                  ),
                  SizedBox(height: 5),
                  Text(
                    '1 Ton-1.5 Ton x2',
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
