from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reports.models import Report

from reports.serializers import (
    ReportSerializer,
)

from reports.permissions import (
    IsAdmin,
)

from posts.models import Post
from users.models import CustomUser


class ReportCreateView(
    APIView
):
  permission_classes = [
      IsAuthenticated
  ]

  def post(
    self,
    request
  ):
    serializer = ReportSerializer(
      data=request.data
    )

    serializer.is_valid(
      raise_exception=True
    )

    report = serializer.save(
      reporter=request.user
    )

    return Response(
      ReportSerializer(
        report
      ).data,
      status=status.HTTP_201_CREATED
    )


class AdminReportListView(
    APIView
):
  permission_classes = [
    IsAdmin
  ]

  def get(
    self,
    request
  ):
    reports = (
      Report.objects.filter(
        status=Report.Status.PENDING
      )
    )

    serializer = (
      ReportSerializer(
        reports,
        many=True
      )
    )

    return Response(
      serializer.data
    )


class AdminReportUpdateView(
  APIView
):
  permission_classes = [
    IsAdmin
  ]

  def patch(
    self,
    request,
    pk
  ):
    report = get_object_or_404(
      Report,
      pk=pk
    )

    status_value = request.data.get(
      "status"
    )

    action = request.data.get(
      "action"
    )

    if status_value not in [
      Report.Status.RESOLVED,
      Report.Status.DISMISSED,
    ]:
      return Response(
        {
          "detail":
          "Status inválido."
        },
        status=status.HTTP_400_BAD_REQUEST,
    )

    if (
      status_value
      ==
      Report.Status.RESOLVED
    ):
      target = report.reported_object

      if (
        isinstance(
          target,
          Post
        )
        and action == "delete"
      ):
        target.delete()

      elif isinstance(
        target,
        CustomUser
      ):

        if action == "deactivate":
          target.is_active = False

          target.save(
            update_fields=[
              "is_active"
            ]
          )

        elif action == "delete":
          target.delete()

    Report.objects.filter(
      pk=report.pk
    ).update(
      status=status_value
    )

    report.refresh_from_db()

    return Response(
      ReportSerializer(
        report
      ).data
    )