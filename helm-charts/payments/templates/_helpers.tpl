{{- define "payments.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "payments.fullname" -}}
{{ include "payments.name" . }}-{{ .Release.Name }}
{{- end }}

{{- define "payments.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}
