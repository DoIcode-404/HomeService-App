import 'package:client/data/constants/constants.dart';
import 'package:client/model/notification_model.dart';
import 'package:client/modules/notifications/components/notification_card.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/list_empty_card.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class NotificationView extends StatelessWidget {
  const NotificationView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: AppSpacing.twentyHorizontal),
        child: Column(
          children: [
            SizedBox(height: 20),
            Row(
              children: [
                const CustomHeaderText(text: 'Notifications'),
                const Spacer(),
                CustomButton(
                  text: 'Recent',
                  icon: AppAssets.kArrowDown,
                  onTap: () {},
                ),
              ],
            ),
            SizedBox(height: 20),
            PrimaryContainer(
              child:
                  notificationsList.isEmpty
                      ? ListEmptyCard(
                        icon: AppAssets.kNoNotification,
                        title: 'No Notifications!',
                        subtitle:
                            'You dont have any notification yet. Please place order',
                        onTap: () {},
                      )
                      : ListView.separated(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemBuilder: (context, index) {
                          return NotificationCard(
                            index: index,
                            notification: notificationsList[index],
                          );
                        },
                        separatorBuilder: (context, index) => const Divider(),
                        itemCount: notificationsList.length,
                      ),
            ),
          ],
        ),
      ),
    );
  }
}
