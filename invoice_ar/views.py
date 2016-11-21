from accounting.models import Transaction
from django.db import transaction
from invoice_ar import models, serializers
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class ContactInvoiceARViewSet(ModelViewSet):
    queryset = models.ContactInvoiceAR.objects.all()
    serializer_class = serializers.ContactInvoiceARSerializer


class CompanyInvoiceARViewSet(ModelViewSet):
    queryset = models.CompanyInvoiceAR.objects.all()
    serializer_class = serializers.CompanyInvoiceARSerializer


class WebServiceSessionViewSet(ModelViewSet):
    queryset = models.WebServiceSession.objects.all()
    serializer_class = serializers.WebServiceSessionSerializer


class PointOfSaleARViewSet(ModelViewSet):
    queryset = models.PointOfSaleAR.objects.all()
    serializer_class = serializers.PointOfSaleARSerializer


class ConceptTypeViewSet(ModelViewSet):
    queryset = models.ConceptType.objects.all()
    serializer_class = serializers.ConceptTypeSerializer


class InvoicesByConceptTypeList(ListAPIView):
    serializer_class = serializers.InvoiceARSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.InvoiceAR.objects.filter(concept_type=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        status = self.request.query_params.get('status')
        pos_type = self.request.query_params.get('pos_type')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)
        if day is not None:
            queryset = queryset.filter(invoice_date__day=day)
        if status is not None:
            queryset = queryset.filter(status=status)
        if pos_type is not None:
            queryset = queryset.filter(
                point_of_sale_ar__point_of_sale_type=pos_type
        ) 

        return queryset


class InvoicesByContactList(ListAPIView):
    serializer_class = serializers.InvoiceARSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.InvoiceAR.objects.filter(invoicear_contact=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        status = self.request.query_params.get('status')
        pos_type = self.request.query_params.get('pos_type')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)
        if day is not None:
            queryset = queryset.filter(invoice_date__day=day)
        if status is not None:
            queryset = queryset.filter(status=status)
        if pos_type is not None:
            queryset = queryset.filter(
                point_of_sale_ar__point_of_sale_type=pos_type
        ) 

        return queryset


class InvoicesByCompanyList(ListAPIView):
    serializer_class = serializers.InvoiceARSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.InvoiceAR.objects.filter(invoicear_company=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        status = self.request.query_params.get('status')
        pos_type = self.request.query_params.get('pos_type')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)
        if day is not None:
            queryset = queryset.filter(invoice_date__day=day)
        if status is not None:
            queryset = queryset.filter(status=status)
        if pos_type is not None:
            queryset = queryset.filter(
                point_of_sale_ar__point_of_sale_type=pos_type
        ) 

        return queryset


class WebServiceSessionsByCompanyList(ListAPIView):
    serializer_class = serializers.WebServiceSessionSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.WebServiceSession.objects.filter(
            invoicear_company=pk
        )


class InvoicesByPointOfSaleARList(ListAPIView):
    serializer_class = serializers.InvoiceARSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = models.InvoiceAR.objects.filter(point_of_sale_ar=pk)

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        if year is not None:
            queryset = queryset.filter(invoice_date__year=year)
        if month is not None:
            queryset = queryset.filter(invoice_date__month=month)
        if day is not None:
            queryset = queryset.filter(invoice_date__day=day)

        return queryset


class InvoiceARViewSet(ModelViewSet):
    queryset = models.InvoiceAR.objects.all()
    serializer_class = serializers.InvoiceARSerializer

    @detail_route(methods=['patch'])
    @transaction.atomic
    def accept(self, request, pk=None):
        invoicear = models.InvoiceAR.objects.get(pk=pk)
        invoicear_company = invoicear.invoicear_company
        if invoicear.status == models.INVOICE_STATUSTYPE_DRAFT:
            debit_account = invoicear_company.default_invoice_debit_account
            credit_account = invoicear_company.default_invoice_credit_account
            transaction = Transaction.objects.create(
                amount=invoicear.total,
                debit_account=debit_account,
                debit_account_balance=debit_account.balance-invoicear.total,
                credit_account=credit_account,
                credit_account_balance=credit_account.balance+invoicear.total,
            )
            invoicear.transaction = transaction
            invoicear.status = models.INVOICE_STATUSTYPE_ACCEPTED
            invoicear.save()
            serializer = serializers.InvoiceARSerializer(
                invoicear,
                context={'request': request}
            )
            return Response(serializer.data, status.HTTP_200_OK)

        return Response({}, status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def authorize(self, request, pk=None):
        invoicear = models.InvoiceAR.objects.get(pk=pk)
        pos_ar_type = invoicear.point_of_sale_ar.point_of_sale_type
        if invoicear.status == models.INVOICE_STATUSTYPE_ACCEPTED and (
            pos_ar_type == models.POINTOFSALE_TYPE_WEBSERVICE
        ):
            invoicear.status = models.INVOICE_STATUSTYPE_AUTHORIZED
            invoicear.save()
            serializer = serializers.InvoiceARSerializer(
                invoicear,
                context={'request': request}
            )
            return Response(serializer.data, status.HTTP_200_OK)

        return Response({}, status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['patch'])
    @transaction.atomic
    def cancel(self, request, pk=None):
        invoicear = models.InvoiceAR.objects.get(pk=pk)
        invoicear_company = invoicear.invoicear_company
        if invoicear.status == models.INVOICE_STATUSTYPE_DRAFT:
            invoicear.status = models.INVOICE_STATUSTYPE_CANCELED
        elif invoicear.status == models.INVOICE_STATUSTYPE_ACCEPTED:
            debit_account = invoicear_company.default_invoice_debit_account
            credit_account = invoicear_company.default_invoice_credit_account
            transaction = Transaction.objects.create(
                amount=invoicear.total,
                debit_account=debit_account,
                debit_account_balance=debit_account.balance-invoicear.total,
                credit_account=credit_account,
                credit_account_balance=credit_account.balance+invoicear.total,
            )
            invoicear.transaction = transaction
            invoicear.status = models.INVOICE_STATUSTYPE_CANCELED
        else:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        invoicear.save()
        serializer = serializers.InvoiceARSerializer(
            invoicear,
            context={'request': request}
        )
        return Response(serializer.data, status.HTTP_200_OK)


class InvoiceARHasVATSubtotalViewSet(ModelViewSet):
    queryset = models.InvoiceARHasVATSubtotal.objects.all()
    serializer_class = serializers.InvoiceARHasVATSubtotalSerializer
