import 'package:client/data/constants/constants.dart';
import 'package:client/modules/categories/components/service_detail_sheet.dart';
import 'package:client/modules/widgets/buttons/custom_text_button.dart';
import 'package:client/modules/widgets/buttons/primary_button.dart';
import 'package:flutter/material.dart';

class ServiceSheet extends StatelessWidget {
  final VoidCallback? saveCallback;
  final VoidCallback? bookCallback;
  final String bookText;
  final bool isDetailPage;
  const ServiceSheet({
    super.key,
    this.saveCallback,
    this.bookCallback,
    required this.bookText,
    this.isDetailPage = false,
  });

  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return Container(
      color: isDarkMode(context) ? Colors.black : AppColors.kWhite,
      padding: EdgeInsets.only(left: 20, right: 20, bottom: 20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              RichText(
                text: TextSpan(
                  text: 'Total:',
                  style: AppTypography.kMedium14.copyWith(
                    color:
                        isDarkMode(context)
                            ? AppColors.kWhite
                            : AppColors.kGrey,
                  ),
                  children: [
                    TextSpan(
                      text: '  USD 150.50',
                      style: AppTypography.kBold14.copyWith(
                        color:
                            isDarkMode(context)
                                ? AppColors.kWhite
                                : Colors.black,
                      ),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              isDetailPage
                  ? CustomTextButton(
                    onPressed: () {
                      showModalBottomSheet(
                        context: context,
                        isScrollControlled: true,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.vertical(
                            top: Radius.circular(20),
                          ),
                        ),
                        builder: (context) {
                          return const ServiceDetailSheet();
                        },
                      );
                    },
                    color: Colors.red,
                    text: 'Bill Details',
                  )
                  : const SizedBox(),
            ],
          ),
          isDetailPage ? const SizedBox() : SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: PrimaryButton(
                  onTap: saveCallback!,
                  text: 'Save Draft',
                  color:
                      isDarkMode(context)
                          ? AppColors.kContentColor
                          : AppColors.kWhite,
                  isBorder: true,
                ),
              ),
              SizedBox(width: 10),
              Expanded(
                child: PrimaryButton(onTap: bookCallback!, text: bookText),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
