import matplotlib.pyplot as plt
import os
import settings


class PlotResult:

    def __init__(self, dict_results, prefix_lenght_list, folder):
        self.dict_results = dict_results
        self.folder = folder
        self.prefix_lenght_list = prefix_lenght_list

    def toPng(self, metric, title):
        plt.clf()
        if metric == "prec-rec":
            # plt.ylim(0.0, 1.05)
            plt.xlabel('Precision', fontsize=18)
            prec = [getattr(res_obj, "precision") for res_obj in self.dict_results]
            rec = [getattr(res_obj, "recall") for res_obj in self.dict_results]
            plt.plot(rec, prec, color=settings.method_color)
        else:
            # plt.ylim(0.0, 1.05)
            plt.xlabel('Prefix length', fontsize=18)
            result_list = [getattr(res_obj, metric) for res_obj in self.dict_results]
            plt.plot(self.prefix_lenght_list, result_list,
                     color=settings.method_color)
            if metric == "gain":
                plt.axhline(y=1, color='k', linestyle='--')
        plt.legend(fontsize=14)
        plt.tight_layout()
        plt.savefig(os.path.join(self.folder, f'{title}.pdf'))