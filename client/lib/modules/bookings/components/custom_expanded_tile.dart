import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class CustomExpandedTile extends StatelessWidget {
  final String title;
  final List<Widget> children;
  const CustomExpandedTile({
    super.key,
    required this.title,
    required this.children,
  });

  @override
  Widget build(BuildContext context) {
    return PrimaryContainer(
      child: Theme(
        data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
        child: ListTileTheme(
          dense: true,
          child: ExpansionTile(
            childrenPadding: EdgeInsets.zero,
            tilePadding: EdgeInsets.zero,
            title: CustomHeaderText(text: title, fontSize: 18),
            children: children,
          ),
        ),
      ),
    );
  }
}
