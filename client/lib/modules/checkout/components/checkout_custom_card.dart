import 'package:client/data/constants/app_assets.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class CheckoutCustomCard extends StatelessWidget {
  final String text;
  final VoidCallback onTap;
  const CheckoutCustomCard({
    super.key,
    required this.text,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: PrimaryContainer(
        child: Row(
          children: [
            CustomHeaderText(text: text, fontSize: 18),
            const Spacer(),
            IgnorePointer(
              ignoring: true,
              child: CustomButton(
                onTap: () {},
                icon: AppAssets.kAddRounded,
                text: 'Add',
                isBorder: true,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
