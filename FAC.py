import classexp
import log as lg
import os
import time
import dataset
import sys
import datetime

while 1:
    try:
        log = lg.log(sys.argv[1])
        log.emailget()
        send_clients = []
        lista_analises = []
        email_send = []
        if log.client_list != 'Nothing to be analysed':
            #criar uma lista com valores unique
            UC = []
            db = dataset.connect('sqlite:///:client_db:')


            a = db.query("SELECT * FROM clients WHERE status=='not_done' LIMIT 1")
            u = [i for i in a]
            id = u[0]['id']
            x = u[0]['client']

            a = db.query("SELECT * FROM clients WHERE id>{0} AND client='{1}' ".format(id,x))
            u = [i for i in a]
            count = len(u)

            months = db.query("SELECT * FROM clients WHERE client='{0}' AND id<='{1}'".format(x,id))

                    
            try:
                print(months)
                dates = [(i['dates'].month,i['dates'].year) for i in months]
                print('~~~~~~Jackin Working')
                print(dates)

                interrompidas_mes = dates.count((datetime.date.today().month, datetime.date.today().year))
            except:

                interrompidas_mes = 1


            
            analise = classexp.Analise(x,sys.argv[2])
            analise.login()
            if analise.country == 'Espanha':
                # send_clients.append(['na',u[0]['client'],analise.country])
                log.loger([['na', x, analise.country]])
                table = db['clients']

                table.update({ 'status':'done', 'id': id}, ['id'] )
                # table.update({'status': 'done', 'id': id}, ['id'])
                db.commit()
                analise.driver.close()
                analise.driver.quit()
                continue
            else:

                while True:
                    try:
                        analise.consolidado()
                    except IndexError as e:
                        print(e)
                        continue
                    break
                while True:
                    try:
                        analise.acc_info()
                    except IndexError as e:
                        print(e)
                        continue
                    break

                while True:
                    try:
                        analise.specific_report(count)
                    except IndexError as e:
                        print(e)
                        continue
                    break
                while not analise.del_completa:
                    try:
                        analise.del_seg()
                    except (IndexError) as e:
                        print(e)
                        break
                num_seg=0
                while num_seg != 3 :
                    # try:
                    print(num_seg)
                    analise.criar_seg(num_seg)
                    num_seg += 1
                    # except:
                    #     pass
                while 1:
                    print('ggg')
                    # try:
                    analise.seg_values()
                    break
                    # except:
                    #     pass

                analise.driver.close()
                analise.driver.quit()
            datahora = 'Análise: {0}, {1} hs'.format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
            send_clients = send_clients + [['a',x,analise.country]]
            save_location = os.path.join(os.path.dirname(__file__),'analises_feitas/{0}/{1}.txt'.format(time.strftime("%d-%m-%Y"),x + ' - ' + analise.campanha[0:15].split('/')[0] + ' - ' + str(time.strftime("%d-%m-%Y"))))
            if not os.path.exists(os.path.join(os.path.dirname(__file__),'analises_feitas/{0}'.format(time.strftime("%d-%m-%Y")))):
                os.makedirs(os.path.join(os.path.dirname(__file__),'analises_feitas/{0}'.format(time.strftime("%d-%m-%Y"))))
            with open(save_location,'w') as f1:
                f1.write(str(datahora) + os.linesep)
                f1.write('Campanha:' + analise.campanha + os.linesep)
                f1.write('Listas de inclusão: {0}'.format(analise.lista[0]) + os.linesep)
                f1.write('Listas de exclusão: {0}'.format(analise.lista[1]) + os.linesep)
                f1.write('Segmentação: {0}'.format(analise.lista[2]) + os.linesep)
                f1.write('Denuncias: {0}'.format(analise.denuncias) + os.linesep)
                f1.write('Cancelamentos: {0}'.format(analise.cance) + os.linesep)
                f1.write('Erros permanentes: {6} ({7}%) - {2} ({3}%) usuários desconhecidos, {0} ({1}%) endereço(s) inativo(s), {4} ({5}%) erros de domínio desconhecido'.format(analise.erros[0], analise.erros[1], analise.erros[2], analise.erros[3], analise.erros[4], analise.erros[5], analise.erros[6], analise.erros[7]) + os.linesep)

                f1.write(os.linesep)
                f1.write('SPF: {0} OK e {1} Falha(s)'.format(analise.spf.count('Autenticado'), analise.spf.count('Falhou')) + os.linesep)
                f1.write('DKIM: {0} OK e {1} Falha(s)'.format(analise.dkim.count('Autenticado'), analise.dkim.count('Falhou')) + os.linesep)
                f1.write('Domínio próprio: {0} de 2 OK'.format(analise.valido) + os.linesep)

                f1.write(os.linesep)
                f1.write("Qualidade de Base: " + analise.quali + os.linesep)
                f1.write("Contatos base: " + analise.cadast + os.linesep)
                f1.write("Campanhas interrompidas no mês: {0}".format(interrompidas_mes) + os.linesep)
                f1.write("Interação 6 meses: {0}".format(analise.segmen[0]) + os.linesep)
                f1.write('Interação 12 meses: {0}'.format(analise.segmen[1]) + os.linesep)
                f1.write('Nunca Interagiram: {0}'.format(analise.segmen[2]) + os.linesep)
                f1.write('Media visualização 3 meses:{0: .2f}%'.format(analise.visua_mean) + os.linesep)
                f1.write('Media clicks 3 meses:{0: .2f}%'.format(analise.clicks_mean) + os.linesep)
            f1.close()
            lista_analises.append(analise)
            email_send.append([save_location, x, analise.campanha[0:15] ])
            log.emailsend([[save_location, x, analise.campanha[0:15] ]])
            # log.loger([['a',x,analise.country]])

            # TODO: inserting API communications with JSON

            # with open(save_location, 'r') as f1:





            # table = db['clients']
            table = db['clients']
            table.update({ 'status': 'done', 'id': id}, ['id'])
            db.commit()


        time.sleep(2)
    except ImportError as e:
        print(e)
        print("something went wrong restarting in 15 secs")
        time.sleep(3)



# datahora = 'Análise: {0}, {1} hs'.format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"))
#

#
#
#
