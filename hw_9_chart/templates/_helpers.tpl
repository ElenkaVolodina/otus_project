{{/*
Expand the name of the chart.
*/}}
{{- define "hw_9_chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "hw_9_chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "hw_9_chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "hw_9_chart.labels" -}}
helm.sh/chart: {{ include "hw_9_chart.chart" . }}
{{ include "hw_9_chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "hw_9_chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "hw_9_chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "hw_9_chart.orderSelectorLabels" -}}
app.kubernetes.io/name: order_service
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "hw_9_chart.hotelSelectorLabels" -}}
app.kubernetes.io/name: hotel_service
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "hw_9_chart.ticketSelectorLabels" -}}
app.kubernetes.io/name: ticket_service
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "hw_9_chart.notifySelectorLabels" -}}
app.kubernetes.io/name: notify_service
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "hw_9_chart.pymentSelectorLabels" -}}
app.kubernetes.io/name: pyment_service
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{/*
Create the name of the service account to use
*/}}
{{- define "hw_9_chart.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "hw_9_chart.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "postgresql.fullname" -}}
{{- printf "%s-%s" .Release.Name "postgresql" | trunc 63 | trimSuffix "-" -}}
{{- end }}