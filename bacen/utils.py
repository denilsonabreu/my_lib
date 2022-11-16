import pandas as pd


class BCB:
    """_summary_
    source: https://www3.bcb.gov.br/sgspub/
    """

    def __init__(self) -> None:
        """_summary_
        """
        self.__name__ = 'BCB_SGS'
        self.codigos = {'selic': [11, 'taxa', 'a.d.'], 'selic_meta': [432, 'taxa', 'a.a.'], 'selic_am': [4390, 'taxa', 'a.m.'], 'cdi': [12, 'taxa', 'a.d.'],
                        'patr_liq_ajus': [21430, 'unidades', 'milhoes'], 'patr_liq_med': [21841, 'unidades', 'milhoes'], 'vendas_var_br': [1455, 'indice', ''],
                        'pib_cor_mes_br': [4380, 'unidades', 'milhoes'],'est_emprego_tot': [28763, 'unidades', ''], 'taxa_desocupacao': [24369, 'taxa', ''], 
                        'pessoas_idade_trab': [24370, 'unidades', 'mil'],'empregados_priv_pub': [24371, 'unidades', 'mil'], 'empregados_pub': [24372, 'unidades', 'mil'],
                        'empregados_proprio': [24373, 'unidades', 'mil'],'empregados_priv_com_car': [24375, 'unidades', 'mil'], 'empregados_priv_sem_car': [24376, 'unidades', 'mil'],
                        'empregados_privado_total': [24377, 'unidades', 'mil'], 'forca_trabalho': [24378, 'unidades', 'mil'], 'pessoas_ocupadas': [24379, 'unidades', 'mil'],
                        'pessoas_desocupadas': [24380, 'unidades', 'mil'], 'ipca': [433, 'taxa', 'a.m.'], 'Papel_moeda_emitido': [1780, 'unidades', 'mil'],
                        'Reservas_bancárias': [1781, 'unidades', 'mil'], 'Base_monetária_restrita':	[1782, 'unidades', 'mil'], 'cred_concessao_tot': [20631, 'unidades', 'milhoes'],
                        'cred_concessao_pj': [20632, 'unidades', 'milhoes'], 'cred_concessao_pf': [20633, 'unidades', 'milhoes'],}

    def consulta_bc(self, codigo: int) -> pd.DataFrame:
        """_summary_

        Args:
            codigo (int): _description_

        Returns:
            pd.DataFrame: _description_
        """
        url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json'
        df = pd.read_json(url)
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df.set_index('data', inplace=True)
        return df

    def get_indicators_list(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        return list(self.codigos.keys())

    def get_indicators_dict(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return {k: v[0] for k, v in self.codigos.items()}

    def get_dataset(self, codigos_dict: dict = None) -> pd.DataFrame:
        """_summary_

        Returns:
            pd.DataFrame: _description_
        """
        
        unidades = list(set([x['unidades'] for x in codigos_dict]))
        taxas = list(filter(lambda x: '%' in x, unidades))
        mil = list(filter(lambda x: 'mil)' in x, unidades))
        milhoes = list(filter(lambda x: 'milhões' in x, unidades))
        
        df = pd.DataFrame()
        # dict_result = {}

        if codigos_dict is None:
            return None
        
        for cod in codigos_dict:
            print(cod['codigo'], cod['nome'], sep=' - ')
            try:
                df_temp = self.consulta_bc(cod['codigo'])
                if cod['unidades'] in taxas:
                    df_temp = df_temp / 100

                if cod['unidades'] in mil:
                    df_temp = df_temp * 1000

                if cod['unidades'] in milhoes:
                    df_temp = df_temp * 1000000

                df_temp.columns = [cod['nome']]
            except:
                df_temp = None
                pass
            
            # dict_result[cod['nome']] = df_temp
            df = pd.concat([df, df_temp], axis=1)

        return df
