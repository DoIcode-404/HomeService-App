import 'package:client/data/constants/constants.dart';
import 'package:client/modules/categories/components/date_card.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class CheckOutDateTimeCard extends StatelessWidget {
  const CheckOutDateTimeCard({super.key});

  @override
  Widget build(BuildContext context) {
    return PrimaryContainer(
      child: Column(
        children: [
          Row(
            children: [
              CustomHeaderText(text: 'Date & Time', fontSize: 18),
              const Spacer(),
              CustomButton(
                text: 'Change',
                icon: AppAssets.kEdit,
                onTap: () {},
                isBorder: true,
              ),
            ],
          ),
          SizedBox(height: 16),
          DateCard(
            onTap: null,
            icon: AppAssets.kDate,
            color: null,
            title: 'Date',
            subtitle: 'November 7, 2021',
          ),
          SizedBox(height: 10),
          DateCard(
            onTap: null,
            icon: AppAssets.kTime,
            color: null,
            title: 'Time',
            subtitle: '12:00-01:00PM',
          ),
        ],
      ),
    );
  }
}
