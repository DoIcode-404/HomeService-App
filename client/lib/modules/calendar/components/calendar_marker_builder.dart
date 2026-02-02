import 'dart:math';

import 'package:client/model/events.dart';
import 'package:flutter/material.dart';

class CustomMarkerBuilder extends StatelessWidget {
  final List<Event> events;

  const CustomMarkerBuilder({super.key, required this.events});

  @override
  Widget build(BuildContext context) {
    if (events.isEmpty) return const SizedBox();

    return ListView.builder(
      shrinkWrap: true,
      scrollDirection: Axis.horizontal,
      itemCount: events.length,
      itemBuilder: (context, index) {
        return Container(
          margin: EdgeInsets.only(top: 25),
          padding: const EdgeInsets.all(1),
          child: Container(
            width: 5,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color:
                  Colors.primaries[Random().nextInt(Colors.primaries.length)],
            ),
          ),
        );
      },
    );
  }
}
