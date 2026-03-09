pipeline {
    agent any

    tools {
      dockerTool 'Docker'
    }
    parameters {
      string(
       name: 'IMAGE_TAG_PYTHON',
       defaultValue: '',
       description: 'Tag de la imagen Docker de python'
      )
      string(
       name: 'IMAGE_TAG_WAF',
       defaultValue: '',
       description: 'Tag de la imagen Docker de waf'
      )
    }
    environment {
      GITHUB_CREDENTIALS = credentials('GitHub')
      DOCKERHUB_CREDENTIALS = credentials('DockerHub1')
      DOCKER_IMAGEPYTHON = 'francesdbz18/pythonb10'
      DOCKER_IMAGEWAF = 'francesdbz18/apacheb10'
      FINAL_IMAGE_TAG_PYTHON = "${params.IMAGE_TAG_PYTHON}"
      FINAL_IMAGE_TAG_WAF = "${params.IMAGE_TAG_WAF}"
      KUBERNETES_HOST = '10.227.87.80'
    }

    stages {
      stage('Clonar repositorio') {
        steps {
          git url: 'https://github.com/pepsamf25/proyectoConcesionario',
          branch: 'main',
          credentialsId: 'GitHub'
        }
      }

      stage('Prueba unitaria') {
        agent {
          docker {
            image 'python:3.11-slim'
            reuseNode true
          }
        }
        steps {
          sh """
        set -e
        python -V
        pip install --no-cache-dir unittest-xml-reporting

        mkdir -p test-results

        # Importante: los módulos (calculos.py, controlador_*.py) están en api/web
        export PYTHONPATH=\$WORKSPACE/api/web
        pip install --no-cache-dir -r api/web/requirements.txt
        python -m xmlrunner discover -s api/web/test -p "test_*.py" -o test-results

        ls -la test-results || true
      """
        }
        post {
          always {
            junit testResults: 'test-results/*.xml', allowEmptyResults: true
          }
      }
      }

      stage('Static Analysis') {
        parallel {
          stage('Detect Secrets') {
            agent {
            docker {
              image "${DOCKER_IMAGEPYTHON}"
              reuseNode true
            }
            }
          steps {
            sh """
            set -e
            pip install --no-cache-dir detect-secrets

            cd \$WORKSPACE/api
            mkdir -p reports

            detect-secrets scan . > reports/detect-secrets-report.json
            """
          }
          post {
            always {
              archiveArtifacts artifacts: 'api/reports/detect-secrets-report.json, api/.secrets.baseline', fingerprint: true
            }
          }
          }
          stage('SonarQube') {
            agent {
                docker {
                  image 'sonarsource/sonar-scanner-cli:latest'
                  reuseNode true
                }
            }
              steps {
                withSonarQubeEnv('sonarqube') {
                  sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=peps-concesionario \
                      -Dsonar.sources=. \
                      -Dsonar.python.version=3.11
                  '''
                }
              }
          }
          stage('SCA') {
            environment {
                NVD_KEY = credentials('NVD_API_KEY')
            }
            agent {
                docker {
              image 'owasp/dependency-check:latest'
              args '--entrypoint="" -u root -v /var/jenkins_home/dependency-check:/usr/share/dependency-check/data'
              reuseNode true
                }
            }
            steps {
                sh '''
                    /usr/share/dependency-check/bin/dependency-check.sh \
                        --project "MiProyecto" \
                        --scan api \
                        --format JSON \
                        --out reports \
                        --nvdApiKey $NVD_KEY
                '''
            }
            post {
                always {
              archiveArtifacts artifacts: 'reports/*', fingerprint: true
                }
            }
          }
        }
      }

      stage('Docker Login') {
        steps {
          withCredentials([usernamePassword(
            credentialsId: 'DockerHub1',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
              sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin' //así no apare la clave en el log
          }
        }
      }

      stage('Build Docker python') {
        steps {
          script {
            dockerImagePython = docker.build("${DOCKER_IMAGEPYTHON}:${FINAL_IMAGE_TAG_PYTHON}", '-f api/Dockerfile api')
          }
        }
      }

      stage('Push Docker python') {
        steps {
          script {
            dockerImagePython.push(FINAL_IMAGE_TAG_PYTHON)
          }
        }
      }

      stage('Scan Docker Image Python for Vulnerabilities') {
        steps {
          script {
            // Escanear la imagen Docker usando docker scan
            sh 'echo aqui va el escaneo de imagen python'
          }
        }
      }

      stage('Build Docker WAF') {
        when {
          expression { params.IMAGE_TAG_WAF?.trim() }
        }
        steps {
          script {
            dockerImageWaf = docker.build("${DOCKER_IMAGEWAF}:${FINAL_IMAGE_TAG_WAF}", '-f apache/Dockerfile apache')
          }
        }
      }

      stage('Push Docker waf') {
        when {
          expression { params.IMAGE_TAG_WAF?.trim() }
        }
        steps {
          script {
            dockerImageWaf.push(FINAL_IMAGE_TAG_WAF)
          }
        }
      }

      stage('Scan Docker Image Waf for Vulnerabilities') {
        when {
          expression { params.IMAGE_TAG_WAF?.trim() }
        }
          steps {
          script {
            // Escanear la imagen Docker
            sh 'echo aqui escaneo imagen waf'
          }
          }
      }

      stage('Run Application with Docker Compose') {
        steps {
          script {
            // Ejecutar la aplicación con Docker Compose
            sh '''
                cat << 'EOF' > .env
                MARIADB_ROOT_PASSWORD=maria@clave$1234
                MARIADB_USER=agenteb10
                MARIADB_USER_PASSWORD=0trab10clave$1234
                MARIADB_DATABASE=concesionario

                DB_USERNAME=grupob10
                DB_PASSWORD=b10clave$1234
                DB_DATABASE=concesionario
                DB_HOST=mariadb
                DB_PORT=3306
                PORT=8090
                HOST=0.0.0.0
                EOF
                '''
            sh '''
                docker compose -f docker-compose.yml up -d
            '''
          }
        }
      }

      stage('End-to-End Tests') {
        agent {
          docker {
            image 'python:3.11-slim'
            reuseNode true
            args '--network pipelinedeploy_default'
          }
        }
        environment {
          APP_URL = 'http://apacheb10:80/'
        }
        steps {
          sh """
        set -e

        pip install --no-cache-dir -r api/web/requirements.txt
        pip install --no-cache-dir selenium>=4.17.0 pytest pytest-html

        apt-get update && apt-get install -y chromium chromium-driver

        export PYTHONPATH=\$WORKSPACE/api/web

        mkdir -p e2e-results

        # Esperar a que apache arranque completamente
        sleep 10

        pytest api/web/tests_e2e \\
          --maxfail=1 --disable-warnings -q \\
          --junitxml=e2e-results/e2e-report.xml --html=e2e-results/report.html --self-contained-html
      """
        }
        post {
          always {
            junit testResults: 'e2e-results/*.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'e2e-results/**', fingerprint: true
          }
        }
      }

      stage('DAST - ZAP Baseline') {
        steps {
          sh '''
        mkdir -p zap-reports
        chmod 777 zap-reports

        docker run --rm \
          -v "$(pwd)/zap-reports:/zap/wrk:rw" \
          --network pipelinedeploy_default \
          --user root \
          ghcr.io/zaproxy/zaproxy:stable \
          zap-baseline.py \
          -t http://apacheb10:80 \
          -r zap-baseline.html \
          -J zap-baseline.json \
          -I
      '''
        }
        post {
          always {
            archiveArtifacts artifacts: 'zap-reports/**', allowEmptyArchive: true, fingerprint: true
          }
        }
      }

      stage('Pruebas IaC') {
        steps {
          script {
            docker.image('bridgecrew/checkov:latest').inside(
              "--network pipelinedeploy_default --entrypoint ''"
            ) {
              sh '''
                checkov \
                  -d ./api \
                  -d ./apache \
                  --framework dockerfile,kubernetes \
                  -o junitxml \
                  --output-file-path checkov-report.xml \
                  --soft-fail
              '''
            }
          }
        }
        post {
          always {
            junit allowEmptyResults: true, testResults: 'checkov-report.xml'
          }
        }
      }

      stage('Deploy en Kubernetes') {
        steps {
          withCredentials([usernamePassword(credentialsId: 'ClaveSSHKubernetes',
                                        usernameVariable: 'JUMP_USER',
                                        passwordVariable: 'JUMP_PASS')]) {
            sh(label: 'Deploy python', script: '''
          set -e
          sshpass -p "$JUMP_PASS" ssh -o StrictHostKeyChecking=no "$JUMP_USER@$KUBERNETES_HOST" 'bash -se' <<EOS
            set -e
            NS=grupob10
            kubectl -n "$NS" set image deployment/python \
              python=${DOCKER_IMAGEPYTHON}:${FINAL_IMAGE_TAG_PYTHON}
            kubectl -n "$NS" rollout status deployment/python --timeout=120s
            EOS
        ''')

            script {
              if (params.IMAGE_TAG_WAF?.trim()) {
                sh(label: 'Deploy waf', script: '''
              set -e
              sshpass -p "$JUMP_PASS" ssh -o StrictHostKeyChecking=no "$JUMP_USER@$KUBERNETES_HOST" 'bash -se' <<EOS
                set -e
                NS=grupob10
                kubectl -n "$NS" set image deployment/apache-waf \
                  apache-waf=${DOCKER_IMAGEWAF}:${FINAL_IMAGE_TAG_WAF}
                kubectl -n "$NS" rollout status deployment/apache-waf --timeout=120s
                EOS
            ''')
          } else {
                echo 'WAF TAG vacío → No se despliega WAF'
              }
            }
                                        }
        }
      }

      stage('Clean Up') {
        steps {
          script {
            // Detener los contenedores después de la prueba
            sh '''
                docker compose down -v
               '''
          }
        }
      }
    }   

        post {
          always {
            script {
                if (env.WORKSPACE) {
              cleanWs()
                } else {
              echo 'No hay workspace, se omite cleanWs'
                }
            }
          }

      success {
        // Enviar notificación o realizar acciones después de la ejecución exitosa
        echo 'Pipeline correcto!'}

      failure {
        // Enviar notificación en caso de fallo
        echo 'Pipeline fallo!'
      }
    }
}
